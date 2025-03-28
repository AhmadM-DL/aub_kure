from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=25, validators=[RegexValidator(r"^[0-9]{6,15}$")])

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    audio_url = models.URLField(blank=True, null=True)
    is_suicidal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Mood(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="moods")
    mood = models.CharField(max_length=50)
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    created_at = models.DateTimeField(auto_now_add=True)

