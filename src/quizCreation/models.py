from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


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
    page = models.ForeignKey(QuizPage, on_delete=models.CASCADE)
    position = models.IntegerField()


class TextElement(models.Model):
    #change to html field
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    content= RichTextField()







