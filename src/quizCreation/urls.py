from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('', views.create_quiz, name="create_quiz"),
    path('edit/<quiz_id>/', views.quiz_edit, name="edit_quiz"),
    path('quiz_page_add/<quiz_id>/', views.quiz_page_add, name="quiz_page_add"),
    path('htmx_create_quiz/', views_htmx.htmx_create_quiz, name="htmx_create_quiz"),
    path('edit/quiz_page/<quiz_id>/<question_id>', views.quiz_page_edit, name="quiz_page_edit"),


]

