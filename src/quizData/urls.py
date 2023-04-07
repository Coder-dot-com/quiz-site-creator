from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('view_quiz_results/<quiz_id>', views.view_quiz_results, name="view_quiz_results"),
    path('delete_response/<quiz_id>/<response_id>', views_htmx.delete_response, name="delete_response"),
    path('detailed_results/<quiz_id>/<response_id>', views.detailed_results, name="detailed_results"),

]