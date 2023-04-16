from django.db import models
from quizCreation.models import UserQuiz

# Create your models here.
pixel_types = [
    ("facebook", "facebook"),
    ("tiktok", "tiktok"),

]


class Pixel(models.Model):
    quiz =  models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    pixel_id = models.CharField(max_length=7000)
    integration_type = models.CharField(max_length=1000, choices=pixel_types)
    conv_api_token = models.CharField(max_length=7000)

