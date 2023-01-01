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
    number = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)


class QuizPageElement(models.Model):
    position = models.IntegerField()


class TitlePageElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    size = models.IntegerField(default=20)






