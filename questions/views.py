import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Question
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from django.contrib import messages

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def create_event(request):
    if request.method == "POST":
        name = request.POST["name"]
        brand_color = request.POST.get("brand_color", "#0d6efd")
        logo = request.FILES.get("logo")

        code = generate_code()
        event = Event.objects.create(
            name=name,
            code=code,
            brand_color=brand_color,
            logo=logo
        )

        NGROK_URL = "https://undelegated-lyman-barefootedly.ngrok-free.dev"
        ask_url = f"{NGROK_URL}/ask/{code}/"

        qr = qrcode.make(ask_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return render(request, "create_event.html", {
            "event": event,
            "qr": qr_base64,
            "ask_url": ask_url
        })

    return render(request, "create_event.html")

def join_event(request, code):
    event = get_object_or_404(Event, code=code)

    if request.method == "POST":
        Question.objects.create(
            event=event,
            text=request.POST["text"]
        )
        return render(request, "thanks.html", {"event": event})

    return render(request, "join.html", {"event": event})


def moderator(request, code):
    event = get_object_or_404(Event, code=code)

    if request.method == "POST":
        q = Question.objects.get(id=request.POST["qid"])
        q.approved = True
        q.save()
        return redirect(request.path)

    questions = Question.objects.filter(event=event, approved=False)
    return render(request, "moderator.html", {
        "event": event,
        "questions": questions
    })


def display(request, code):
    event = get_object_or_404(Event, code=code)
    questions = Question.objects.filter(event=event, approved=True)
    return render(request, "display.html", {
        "event": event,
        "questions": questions
    })

def download_qr(request, code):
    event = get_object_or_404(Event, code=code)

    NGROK_URL = "https://abc123.ngrok-free.app"
    join_url = f"{NGROK_URL}/join/{code}/"

    qr = qrcode.make(join_url).convert("RGB")

    # Create canvas
    width, height = qr.size
    canvas = Image.new("RGB", (width, height + 120), "white")
    canvas.paste(qr, (0, 60))

    draw = ImageDraw.Draw(canvas)

    # Brand color bar
    draw.rectangle([0, 0, width, 50], fill=event.brand_color)
    draw.text((width // 2 - 100, 15), "SCAN TO ASK A QUESTION", fill="white")

    # Add logo if exists
    if event.logo:
        logo = Image.open(event.logo.path)
        logo.thumbnail((80, 80))
        canvas.paste(logo, (10, 60))

    response = HttpResponse(content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="{event.name}_QR.png"'

    canvas.save(response, "PNG")
    return response

def ask_question(request, event_code):
    event = get_object_or_404(Event, code=event_code)

    if request.method == "POST":
        Question.objects.create(
            event=event,
            text=request.POST.get("text")
        )
        messages.success(request, "Question sent ✔️ Ask another.")
        return redirect("ask_question", event_code=event.code)

    return render(request, "ask_question.html", {
        "event": event
    })