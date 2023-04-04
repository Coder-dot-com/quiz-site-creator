from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('preview_quiz/<quiz_id>/', views.preview_quiz, name="preview_quiz"),


    path('next_page_quiz/<quiz_id>/<number>/', views_htmx.next_page_preview, name="next_page_quiz_preview"),
    path('previous_page_preview/<quiz_id>/<number>/', views_htmx.previous_page_preview, name="previous_page_preview"),
    
    path('take_quiz/<quiz_id>/', views.take_quiz, name="take_quiz"),

]