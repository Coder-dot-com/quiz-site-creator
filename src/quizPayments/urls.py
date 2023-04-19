from django.urls import path
from . import views, views_htmx

urlpatterns = [

    path('add_stripe_integration/<quiz_id>', views_htmx.add_stripe_integration, name="add_stripe_integration"),
    path('delete_stripe_integration/<quiz_id>', views_htmx.delete_stripe_integration, name="delete_stripe_integration"),
    
    path('get_create_product_form/<quiz_id>', views_htmx.get_create_product_form, name="get_create_product_form"),
    path('create_product/<quiz_id>', views_htmx.create_product, name="create_product"),


]