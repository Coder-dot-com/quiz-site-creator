from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('preview_quiz/<quiz_id>/<quiz_page>/', views_htmx.preview_quiz_page, name="preview_quiz_page"),
    path('preview_quiz/<quiz_id>/', views.preview_quiz, name="preview_quiz"),

]