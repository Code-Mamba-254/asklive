from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)

    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    brand_color = models.CharField(
        max_length=7, default="#0d6efd"
    )  # Bootstrap blue

    def __str__(self):
        return f"{self.name} ({self.code})"


class Question(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    