from django.db import models
from quizCreation.models import UserQuiz, QuizPageElement, MultipleChoiceChoice
from session_management.models import UserSession

# Create your models here.

 
class Response(models.Model):
    quiz = models.ForeignKey(UserQuiz, on_delete=models.SET_NULL, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    response_id = models.CharField(max_length=500, unique=True)
    session = models.ForeignKey(UserSession, on_delete=models.SET_NULL, null=True, related_name='quizRenderSession')
    steps_completed = models.CharField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    # purchased = models.BooleanField(default=False)

  
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizPageElement, on_delete=models.SET_NULL, null=True)
    question_choice = models.ManyToManyField(MultipleChoiceChoice, blank=True, null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=5000)

