from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('', views.create_quiz, name="create_quiz"),
    path('edit/<quiz_id>/', views.quiz_edit, name="edit_quiz"),
    path('quiz_page_add/<quiz_id>/', views.quiz_page_add, name="quiz_page_add"),
    path('htmx_create_quiz/', views_htmx.htmx_create_quiz, name="htmx_create_quiz"),
    path('edit/quiz_page/<quiz_id>/<page_id>', views.quiz_page_edit, name="quiz_page_edit"),
    path('edit/all_element_swatches/<quiz_id>/<page_id>', views_htmx.all_element_swatches, name="all_element_swatches"),

    path('quiz_page_element_add/<quiz_id>/<page_id>', views_htmx.quiz_page_element_add, name="quiz_page_element_add"),

    path('add_text_element/<quiz_id>/<page_id>', views_htmx.add_text_element, name="add_text_element"),
    path('move_page_up/<quiz_id>/<page_id>', views_htmx.move_page_up, name="move_page_up"),
    path('move_page_down/<quiz_id>/<page_id>', views_htmx.move_page_down, name="move_page_down"),
    path('delete_quiz_page/<quiz_id>/<page_id>', views_htmx.delete_quiz_page, name="delete_quiz_page"),

    path('get_quiz_page_elements/<quiz_id>/<page_id>', views_htmx.get_quiz_page_elements, name="get_quiz_page_elements"),
    path('delete_page_element/<quiz_id>/<page_id>/<element_id>', views_htmx.delete_page_element, name="delete_page_element"),
    
    path('move_element_up/<quiz_id>/<page_id>/<element_id>', views_htmx.move_element_up, name="move_element_up"),
    path('move_element_down/<quiz_id>/<page_id>/<element_id>', views_htmx.move_element_down, name="move_element_down"),

    path('edit_element_modal/<quiz_id>/<page_id>/<element_id>', views_htmx.edit_element_modal, name="edit_element_modal"),

    path('edit_text_element/<quiz_id>/<page_id>/<element_id>', views_htmx.edit_text_element, name="edit_text_element"),

]

