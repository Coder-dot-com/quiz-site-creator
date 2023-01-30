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
        char_input_element = CharInputElement.objects.filter(page_element=self)
        if char_input_element.exists():
            return {'type': 'Char input element', 'element': char_input_element[0]}
        text_input_element = TextInputElement.objects.filter(page_element=self)
        if text_input_element.exists():
            return {'type': 'Text input element', 'element': text_input_element[0]}
        email_input_element = EmailInputElement.objects.filter(page_element=self)
        if email_input_element.exists():
            return {'type': 'Email input element', 'element': email_input_element[0]}
        number_input_element = NumberInputElement.objects.filter(page_element=self)
        if number_input_element.exists():
            return {'type': 'Number input element', 'element': number_input_element[0]}
        multiple_choice = MultipleChoiceElement.objects.filter(page_element=self)
        if multiple_choice.exists():
            return {'type': 'Multiple choice question', 'element': multiple_choice[0]}


class TextElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    content = RichTextField()

class CharInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class TextInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class EmailInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class NumberInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class MultipleChoiceElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class MultipleChoiceChoice(models.Model):
    multiple_choice_element = models.ForeignKey(MultipleChoiceElement, on_delete=models.CASCADE)
    choice = models.CharField(max_length=300)