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
    name = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)

    def get_quiz_page_elements(self):
        return QuizPageElement.objects.filter(page=self).order_by('position')


class QuizPageElement(models.Model):
    page = models.ForeignKey(QuizPage, on_delete=models.CASCADE)
    position = models.IntegerField()

    def get_element_type(self):
        text_element = TextElement.objects.filter(page_element=self)
        if text_element.exists():
            return {'type': 'Text element', 'element': text_element[0]}


class TextElement(models.Model):
    #change to html field
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    content= RichTextField()







