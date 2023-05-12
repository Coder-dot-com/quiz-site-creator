from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget

User = get_user_model() 
# Create your models here.

class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='user_quiz_logos/', null=True, blank=True)
    analytics_scripts = models.TextField(max_length=10000, null=True, blank=True)
    redirect_url = models.URLField(max_length=10000, null=True, blank=True)
    quiz_confirmation_content = RichTextUploadingField(null=True, blank=True)
    stripe_public_key = models.CharField(max_length=10000, null=True, blank=True)
    stripe_secret_key = models.CharField(max_length=10000, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_code/', null=True, blank=True)




#html field with image ckeditor
#redirect url
#
    def first_quiz_page(self):
        return QuizPage.objects.filter(quiz=self).order_by('number').first()
    
    def next_quiz_page(self, number):
        return QuizPage.objects.filter(quiz=self, number__gt=number).order_by('number').first()

    def previous_quiz_page(self, number):
        a =  QuizPage.objects.filter(quiz=self, number__lt=number).order_by('number')
        print(a)

        return a.last()
    

    def get_num_of_quiz_pages(self):
        return int(QuizPage.objects.filter(quiz=self).order_by('-number')[0].number)
    
    def get_all_questions(self):

        quiz_page_elements = []

        for i in range(1, self.get_num_of_quiz_pages() + 1):
            quiz_page =  QuizPage.objects.get(quiz=self, number=i)
            quiz_page_elements.append(quiz_page.get_quiz_page_elements())
        return quiz_page_elements

        
    


class QuizPage(models.Model):
    quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    number = models.IntegerField()
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
            return {'type': 'Text', 'element': text_element[0]}  
        image_display_element = ImageDisplayElement.objects.filter(page_element=self)
        if image_display_element.exists():
            return {'type': 'Image', 'element': image_display_element[0]}
        char_input_element = CharInputElement.objects.filter(page_element=self)
        if char_input_element.exists():
            return {'type': 'Char input', 'element': char_input_element[0]}
        text_input_element = TextInputElement.objects.filter(page_element=self)
        if text_input_element.exists():
            return {'type': 'Text input', 'element': text_input_element[0]}
        email_input_element = EmailInputElement.objects.filter(page_element=self)
        if email_input_element.exists():
            return {'type': 'Email input', 'element': email_input_element[0]}
        
        number_input_element = NumberInputElement.objects.filter(page_element=self)
        if number_input_element.exists():
            return {'type': 'Number input', 'element': number_input_element[0]}
        
        review_stars_element = ReviewStars.objects.filter(page_element=self)
        if review_stars_element.exists():
            return {'type': 'Review stars', 'element': review_stars_element[0]}
        
        multiple_choice = MultipleChoiceElement.objects.filter(page_element=self)
        if multiple_choice.exists():
            return {'type': 'Multiple choice question', 'element': multiple_choice[0]}
        single_choice = SingleChoiceElement.objects.filter(page_element=self)
        if single_choice.exists():
            return {'type': 'Single choice question', 'element': single_choice[0]}
        agree_disagree_element = AgreeDisagree.objects.filter(page_element=self)
        if agree_disagree_element.exists():
            return {'type': 'Agree disagree table', 'element': agree_disagree_element[0]}
        satisfied_unsatisfied = SatisfiedUnsatisfied.objects.filter(page_element=self)
        if satisfied_unsatisfied.exists():
            return {'type': 'Satisfied unsatisfied table', 'element': satisfied_unsatisfied[0]}        



class ImageDisplayElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_quiz_images/')

class TextElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    content = RichTextUploadingField()



class CharInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)

class TextInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)

class EmailInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)

    use_as_email_for_conversion_tracking = models.BooleanField(default=False)  

class NumberInputElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)


class MultipleChoiceElement(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)


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
    required = models.BooleanField(default=False)


    def get_single_choice_choices(self):
        return SingleChoiceChoice.objects.filter(single_choice_element=self)

class SingleChoiceChoice(models.Model):
    single_choice_element = models.ForeignKey(SingleChoiceElement, on_delete=models.CASCADE)
    choice = models.CharField(max_length=300)
    is_correct_choice = models.BooleanField(default=False)
    image = models.ImageField(upload_to="choice_images/", null=True, blank=True)



class AgreeDisagree(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=True, blank=True)

    def get_rows(self):
        return AgreeDisagreeRow.objects.filter(agree_disagree_element=self).order_by('position')


class AgreeDisagreeRow(models.Model):
    agree_disagree_element = models.ForeignKey(AgreeDisagree, on_delete=models.CASCADE)
    position = models.IntegerField()
    title = models.TextField(max_length=10000)
    required = models.BooleanField(default=False)

  

class SatisfiedUnsatisfied(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=True, blank=True)

    def get_rows(self):
        return SatisfiedUnsatisfiedRow.objects.filter(satisfied_unsatisfied_element=self).order_by('position')


class SatisfiedUnsatisfiedRow(models.Model):
    satisfied_unsatisfied_element = models.ForeignKey(SatisfiedUnsatisfied, on_delete=models.CASCADE)
    position = models.IntegerField()
    title = models.TextField(max_length=10000)
    required = models.BooleanField(default=False)


class ReviewStars(models.Model):
    page_element = models.OneToOneField(QuizPageElement, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    required = models.BooleanField(default=False)