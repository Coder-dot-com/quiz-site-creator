from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('', views.create_quiz, name="create_quiz"),
    path('edit/<quiz_id>/', views.quiz_edit, name="edit_quiz"),
    path('htmx_create_quiz/', views_htmx.htmx_create_quiz, name="htmx_create_quiz"),

]

