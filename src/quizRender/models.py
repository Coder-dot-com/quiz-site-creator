from django.db import models
from quizCreation.models import UserQuiz, QuizPageElement, MultipleChoiceChoice, AgreeDisagreeRow, SingleChoiceChoice, DropdownChoice, SatisfiedUnsatisfiedRow
from session_management.models import UserSession
from itertools import chain
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
    
    def get_all_answers(self):
        list_of_pages =  Answer.objects.filter(response=self).order_by('question__page').values_list('question__page').distinct()
        ordered_questions = []
        for i in list_of_pages:
            a = Answer.objects.filter(response=self, question__page=i).order_by('question__position')
            ordered_questions.append(a)
        return ordered_questions
  
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizPageElement, on_delete=models.SET_NULL, null=True, blank=True)
    question_agree_disagree = models.ForeignKey(AgreeDisagreeRow, on_delete=models.SET_NULL, null=True, blank=True)
    question_satisfied_unsatisfied = models.ForeignKey(SatisfiedUnsatisfiedRow, on_delete=models.SET_NULL, null=True, blank=True)
    question_choice = models.ManyToManyField(MultipleChoiceChoice, blank=True, null=True)
    single_question_choice = models.ForeignKey(SingleChoiceChoice, blank=True, null=True, on_delete=models.SET_NULL)
    dropdown_choice = models.ForeignKey(DropdownChoice, blank=True, null=True, on_delete=models.SET_NULL)
    time_added = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=5000)

