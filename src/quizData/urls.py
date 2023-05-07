from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('view_quiz_results/<quiz_id>', views.view_quiz_results, name="view_quiz_results"),
    path('delete_response/<quiz_id>/<response_id>', views_htmx.delete_response, name="delete_response"),
    path('delete_response_detail/<quiz_id>/<response_id>', views.delete_response_detail, name="delete_response_detail"),


    
    path('detailed_results/<quiz_id>/<response_id>', views.detailed_results, name="detailed_results"),

    path('download_csv_of_responses/<quiz_id>', views.download_csv_of_responses, name="download_csv_of_responses"),

    path('question_by_question_breakdown/<quiz_id>', views.question_by_question_breakdown, name="question_by_question_breakdown"),
    path('get_question_answers/<quiz_id>/<question_id>', views_htmx.get_question_answers, name="get_question_answers"),



]