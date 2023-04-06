from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('view_quiz_results/<quiz_id>', views.view_quiz_results, name="view_quiz_results"),

]