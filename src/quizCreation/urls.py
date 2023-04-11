from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('', views.create_quiz, name="create_quiz"),
    path('edit/<quiz_id>/', views.quiz_edit, name="edit_quiz"),
    path('delete/<quiz_id>/', views_htmx.htmx_quiz_delete, name="htmx_quiz_delete"),
    # path('duplicate_quiz/<quiz_id>/', views_htmx.duplicate_quiz, name="duplicate_quiz"),


    path('quiz_page_add/<quiz_id>/', views.quiz_page_add, name="quiz_page_add"),
    path('htmx_create_quiz/', views_htmx.htmx_create_quiz, name="htmx_create_quiz"),
    path('edit/quiz_page/<quiz_id>/<page_id>', views.quiz_page_edit, name="quiz_page_edit"),
    path('edit/all_element_swatches/<quiz_id>/<page_id>', views_htmx.all_element_swatches, name="all_element_swatches"),

    path('quiz_page_element_add/<quiz_id>/<page_id>', views_htmx.quiz_page_element_add, name="quiz_page_element_add"),

    path('add_text_element/<quiz_id>/<page_id>', views_htmx.add_text_element, name="add_text_element"),
    path('add_text_input_element/<quiz_id>/<page_id>', views_htmx.add_text_input_element, name="add_text_input_element"),
    path('add_char_input_element/<quiz_id>/<page_id>', views_htmx.add_char_input_element, name="add_char_input_element"),
    path('add_email_input_element/<quiz_id>/<page_id>', views_htmx.add_email_input_element, name="add_email_input_element"),
    path('add_number_input_element/<quiz_id>/<page_id>', views_htmx.add_number_input_element, name="add_number_input_element"),
    path('add_multiple_choice_element/<quiz_id>/<page_id>', views_htmx.add_multiple_choice_element, name="add_multiple_choice_element"),
    
    path('add_single_choice_element/<quiz_id>/<page_id>', views_htmx.add_single_choice_element, name="add_single_choice_element"),


    path('move_page_up/<quiz_id>/<page_id>', views_htmx.move_page_up, name="move_page_up"),
    path('move_page_down/<quiz_id>/<page_id>', views_htmx.move_page_down, name="move_page_down"),
    path('delete_quiz_page/<quiz_id>/<page_id>', views_htmx.delete_quiz_page, name="delete_quiz_page"),



    path('get_quiz_page_elements/<quiz_id>/<page_id>', views_htmx.get_quiz_page_elements, name="get_quiz_page_elements"),
    path('delete_page_element/<quiz_id>/<page_id>/<element_id>', views_htmx.delete_page_element, name="delete_page_element"),
    

    path('add_choice_to_multiple_choice_element/<quiz_id>/<page_id>/<element_id>', views_htmx.add_choice_to_multiple_choice_element, name="add_choice_to_multiple_choice_element"),

    path('add_choice_to_single_choice_element/<quiz_id>/<page_id>/<element_id>', views_htmx.add_choice_to_single_choice_element, name="add_choice_to_single_choice_element"),


    path('get_text_element_edit_form/<quiz_id>/<element_id>', views_htmx.get_text_element_edit_form, name="get_text_element_edit_form"),

    path('edit_text_input_element/<quiz_id>/<element_id>', views_htmx.edit_text_input_element, name="edit_text_input_element"),



    path('delete_choice_multiple_choice_element/<quiz_id>/<page_id>/<element_id>/<choice_id>', views_htmx.delete_choice_multiple_choice_element, name="delete_choice_multiple_choice_element"),
    path('delete_choice_single_choice_element/<quiz_id>/<page_id>/<element_id>/<choice_id>', views_htmx.delete_choice_single_choice_element, name="delete_choice_single_choice_element"),


    path('move_element_up/<quiz_id>/<page_id>/<element_id>', views_htmx.move_element_up, name="move_element_up"),
    path('move_element_down/<quiz_id>/<page_id>/<element_id>', views_htmx.move_element_down, name="move_element_down"),

    path('edit_element_title/<quiz_id>/<page_id>/<element_id>', views_htmx.edit_element_title, name="edit_element_title"),
    
    path('upload_quiz_logo/<quiz_id>/', views_htmx.upload_quiz_logo, name="upload_quiz_logo"),
    path('delete_logo_from_quiz/<quiz_id>/', views_htmx.delete_logo_from_quiz, name="delete_logo_from_quiz"),
    path('update_quiz_analytic_scripts/<quiz_id>/', views_htmx.update_quiz_analytic_scripts, name="update_quiz_analytic_scripts"),


]

