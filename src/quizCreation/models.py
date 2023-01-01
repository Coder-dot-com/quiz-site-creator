from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)


class QuizPage(models.Model):
    quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
