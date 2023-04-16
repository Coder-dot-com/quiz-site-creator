from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('add_fb_tiktok_capi/<quiz_id>', views_htmx.add_fb_tiktok_capi, name="add_fb_tiktok_capi"),
    path('delete_fb_tiktok_capi/<quiz_id>/<pixel_id>', views_htmx.delete_fb_tiktok_capi, name="delete_fb_tiktok_capi")

]

