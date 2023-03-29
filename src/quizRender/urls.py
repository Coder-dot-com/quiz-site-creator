from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('preview_quiz/<quiz_id>/', views_htmx.preview_quiz, name="preview_quiz"),

]