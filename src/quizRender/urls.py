from django.urls import path
from . import views, views_htmx

urlpatterns = [

    #preview
    path('preview_quiz/<quiz_id>/', views.preview_quiz, name="preview_quiz"),
    path('next_page_quiz/<quiz_id>/<number>/', views_htmx.next_page_preview, name="next_page_quiz_preview"),
    path('previous_page_preview/<quiz_id>/<number>/', views_htmx.previous_page_preview, name="previous_page_preview"),
    

    #take quiz
    path('take_quiz/<quiz_id>/', views.take_quiz, name="take_quiz"),
    path('take_next_page_quiz/<quiz_id>/<number>/<response_id>', views_htmx.take_next_page, name="take_next_page"),
    path('take_previous_page/<quiz_id>/<number>/<response_id>', views_htmx.take_previous_page, name="take_previous_page"),
    
    
    path('get_value_stored_in_db/<quiz_id>/<element_id>/<response_id>', views_htmx.get_value_stored_in_db, name="get_value_stored_in_db"),
    path('get_value_stored_in_db/<quiz_id>/<element_id>/<response_id>/<question_id>', views_htmx.get_value_stored_in_db, name="get_value_stored_in_db_agree_disagree"),

    path('complete_quiz/<quiz_id>/<number>/<response_id>', views.complete_quiz, name="complete_quiz"),


]