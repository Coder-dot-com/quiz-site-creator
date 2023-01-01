
from django.contrib import admin
from django.urls import include, path
from . import views, views_htmx

urlpatterns = [
    path('quiz_without_question_num/<unique_id>/', views_htmx.quiz_without_question_num, name="quiz_without_question_num"),
    path('submit_question/<unique_id>/<question_id>/', views_htmx.submit_question, name="submit_question"),
    path('go_back_question/<unique_id>/<question_id>/<response>/', views_htmx.go_back_question, name="go_back_question"),
    path('image_upload/<unique_id>/<question_id>/<response_id>/', views_htmx.image_upload, name="image_upload"),
    path('<unique_id>/upload_image/<response_id>/<user_image_id>/', views_htmx.delete_image, name="delete_image"),
    path('payment_success/', views.quiz_payment_success, name="quiz_payment_success"),
    path('checkout/<unique_id>/<response_id>/', views_htmx.checkout, name="quiz_checkout"),
    path('go_back_quiz_end/<unique_id>/<response>/', views_htmx.go_back_quiz_end, name="go_back_quiz_end"),
    path('go_back_purchase/<response_id>/', views_htmx.go_back_purchase, name="go_back_purchase"),

    path('chosen_currency_quiz_end/<currency_code>/<response_id>', views_htmx.chosen_currency_quiz_end, name='chosen_currency_quiz_end'),
]

