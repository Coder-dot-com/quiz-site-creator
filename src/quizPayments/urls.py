from django.urls import path
from . import views, views_htmx

urlpatterns = [

    path('add_stripe_integration/<quiz_id>', views_htmx.add_stripe_integration, name="add_stripe_integration"),
    path('delete_stripe_integration/<quiz_id>', views_htmx.delete_stripe_integration, name="delete_stripe_integration"),
    
    path('add_product_quiz/<quiz_id>', views.add_product_quiz, name="add_product_quiz"),
    path('create_product/<quiz_id>', views.create_product, name="create_product"),
    path('delete_product_quiz/<quiz_id>', views.delete_product_quiz, name="delete_product_quiz"),
    path('add_image_quiz_product/<quiz_id>', views_htmx.add_image_quiz_product, name="add_image_quiz_product"),
    path('delete_image_quiz_product/<quiz_id>/<image_id>', views_htmx.delete_image_quiz_product, name="delete_image_quiz_product"),



]