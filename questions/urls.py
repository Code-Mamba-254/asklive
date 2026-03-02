from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_event, name="create_event"),
    path("join/<str:code>/", views.join_event, name="join_event"),
    path("mod/<str:code>/", views.moderator, name="moderator"),
    path("display/<str:code>/", views.display, name="display"),
    path("qr/<str:code>/download/", views.download_qr, name="download_qr"),
    path("ask/<str:event_code>/", views.ask_question, name="ask_question"),
]
