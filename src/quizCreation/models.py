from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model()
# Create your models here.

class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='user_quiz_logos/', null=True, blank=True)
    analytics_scripts = models.TextField(max_length=10000, null=True, blank=True)

    def first_quiz_page(self):
        return QuizPage.objects.filter(quiz=self).order_by('number').first()
    
    def next_quiz_page(self, number):
        return QuizPage.objects.filter(quiz=self, number__gt=number).order_by('number').first()

    def previous_quiz_page(self, number):
        a =  QuizPage.objects.filter(quiz=self, number__lt=number).order_by('number')
        print(a)

        return a.last()
    


class QuizPage(models.Model):
    quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)

    def get_quiz_page_elements(self):
        return QuizPageElement.objects.filter(page=self).order_by('position')
    

    def is_last_page(self):
        if QuizPage.objects.filter(quiz=self.quiz, number__gt=self.number).exists():
            return False
        else:
            return True


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
        single_choice = SingleChoiceElement.objects.filter(page_element=self)
        if single_choice.exists():
            return {'type': 'Single choice question', 'element': single_choice[0]}
        agree_disagree_element = AgreeDisagree.objects.filter(page_element=self)
        if agree_disagree_element.exists():
            return {'type': 'Agree disagree element', 'element': agree_disagree_element[0]}


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
    use_as_email_for_conversion_tracking = models.BooleanField(default=False)  
class NumberInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class MultipleChoiceElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)


    def get_multiple_choice_choices(self):
        return MultipleChoiceChoice.objects.filter(multiple_choice_element=self)

class MultipleChoiceChoice(models.Model):
    multiple_choice_element = models.ForeignKey(MultipleChoiceElement, on_delete=models.CASCADE)
    choice = models.CharField(max_length=300)
    is_correct_choice = models.BooleanField(default=False)
    image = models.ImageField(upload_to="choice_images/", null=True, blank=True)

class SingleChoiceElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)


    def get_single_choice_choices(self):
        return SingleChoiceChoice.objects.filter(single_choice_element=self)

class SingleChoiceChoice(models.Model):
    single_choice_element = models.ForeignKey(SingleChoiceElement, on_delete=models.CASCADE)
    choice = models.CharField(max_length=300)
    is_correct_choice = models.BooleanField(default=False)
    image = models.ImageField(upload_to="choice_images/", null=True, blank=True)



class AgreeDisagree(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class AgreeDisagreeRow(models.Model):
    agree_disagree_element = models.ForeignKey(AgreeDisagree, on_delete=models.CASCADE)
    position = models.IntegerField()
    title = models.TextField(max_length=10000)

  

