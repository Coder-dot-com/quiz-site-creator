from uuid import uuid4
from django.db import models
from emails.models import UserEmail
from multicurrency.models import Currency
from session_management.models import Category, UserSession
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserPreferenceType
from tinymce.models import HTMLField
from datetime import datetime, timedelta, timezone
from quiz_site.settings import AWS_STORAGE_BUCKET_NAME

User = get_user_model()

product_types = [
    ("once_only", "once_only"),
    ("user_chosen", "user_chosen"),
]

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=300, default="once_only", choices=product_types)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    price_without_discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    created_date =  models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    num_sold = models.IntegerField(default=0)



    def __str__(self) -> str:
        return self.name

    



quiz_type_choices = [
    ("setUserPreferences", "setUserPreferences"),
    ("feedback", "feedback"),
    ("updateUserPreferences", "updateUserPreferences"),
]

# Create your models here.
class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    quiz_type = models.CharField(default="setUserPreferences", max_length=300, choices=quiz_type_choices)

    name = models.CharField(max_length=300, unique=True)
    display_name = models.CharField(max_length=300)
    ending = HTMLField(max_length=10000, null=True, blank=True)

    unique_id = models.CharField(max_length=400, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_questions(self):
        return Question.objects.filter(quiz=self).order_by('question_number')

    #Need to auto generate unique id and link on save

    def save(self, *args, **kwargs):

        if not self.unique_id:
            self.unique_id = str(uuid4())
            

        super(Quiz, self).save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse('quiz', args=[self.unique_id])

    


question_types = [
    ("Single Choice", "Single Choice"),
    ("Multiple Choice", "Multiple Choice"),
    ("Text Input", "Text Input"),
    ("Char Input", "Char Input"),
    ("Image Input", "Image Input"),
    ("Email Input", "Email Input"),
    ("password", "password"),
    ("Sales Page", "Sales Page"),


]

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    #-question is then foreign keyed optionally to userpreference name
    user_preference_type = models.ForeignKey(UserPreferenceType, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=300, choices=question_types)

    title = models.CharField(max_length=400)
    number = models.IntegerField()
    description = HTMLField(max_length=10000, null=True, blank=True)
    skippable = models.BooleanField(default=False)
    image = models.ImageField(upload_to='quiz/images', null=True, blank=True)
    input_placeholder = models.CharField(max_length=300, null=True, blank=True)
    image_upload_number = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.quiz} | {self.title}"

    
    def get_question_choices(self):
        return QuestionChoice.objects.filter(question=self)


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    option_image_icon = models.ImageField(upload_to='question_choice_images/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.option
    

class Response(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    response_id = models.CharField(max_length=500, unique=True)
    session = models.ForeignKey(UserSession, on_delete=models.SET_NULL, null=True)
    steps_completed = models.CharField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

  
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    question_choice = models.ManyToManyField(QuestionChoice, blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=5000)

    def get_user_images(self):
        return UserImageUpload.objects.filter(answer=self)


class UserImageUpload(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_uploads/")

    def more_than_2_mins_since_created(self):
        # Wait for cleaned image if more than 2 mins then use cleaned image else use other
        if datetime.now(timezone.utc) > self.time_created + timedelta(minutes=2):
            return True
        else:
            return False

    def cleaned_image(self):
        
        file_name = str(self.image.name)

        if file_name:
            return(f"https://{AWS_STORAGE_BUCKET_NAME}-resized.s3.us-west-1.amazonaws.com/{file_name}")
        else:
            pass

status_choices = [
    ("created", "created"),
    ("paid", "paid"),
]
class QuizOrder(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=300, choices=status_choices, default="created")
    session = models.ForeignKey(UserSession, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user_chosen_price_per_month =  models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    user_chosen_interval_months = models.IntegerField(null=True, blank=True)
    response = models.ForeignKey(Response, on_delete=models.SET_NULL, null=True)
    email = models.ForeignKey(UserEmail, on_delete=models.SET_NULL, null=True)
    order_total =  models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    total_usd = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=500, null=True, blank=True)
    order_number = models.CharField(max_length=500, null=True, blank=True)
    email_sent = models.BooleanField(default=False)