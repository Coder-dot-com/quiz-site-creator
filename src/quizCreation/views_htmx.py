from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import UserQuiz, QuizPage, QuizPageElement, TextElement, MultipleChoiceChoice, MultipleChoiceElement, SingleChoiceChoice, SingleChoiceElement, AgreeDisagree, AgreeDisagreeRow
from .forms import TextElementForm, CharInputElementForm, TextInputElementForm, EmailInputElementForm, NumberInputElementForm, MultipleChoiceElementForm, MultipleChoiceChoiceForm, SingleChoiceElementForm, SingleChoiceChoiceForm, AgreeDisagreeElementForm, AgreeDisagreeRowForm
from django.urls import reverse
import os
from uuid import uuid4
from django.utils.datastructures import MultiValueDictKeyError

@login_required
def htmx_create_quiz(request):
    quiz_name = request.POST['quiz_name']
    user_quiz = UserQuiz.objects.create(name=quiz_name, user=request.user)

    context = {
        'user_quiz': user_quiz,
        'hx_url': f"/create_quiz/edit/{user_quiz.id}",
    }

    return render(request, 'questions_page.html', context=context)


@login_required
def htmx_quiz_delete(request, quiz_id):

    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id).delete()

    user_quizes_list = UserQuiz.objects.filter(user=request.user)
    context = {
        'quizes': user_quizes_list,
    }
    return render(request, 'quiz_creation/quizes_list.html', context=context)




@login_required
def quiz_page_element_add(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.filter(quiz=user_quiz, id=page_id)
        if quiz_page.exists():
            quiz_page = quiz_page[0]
        # don't create the object yet just determine which element the user selected
        #  and pass the required form
            element = request.POST['element']

            if element == "text":
                form = TextElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }

                return render(request, 'element_forms/text.html', context=context)

            elif element == "CharInput":

                form = CharInputElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/CharInput.html', context=context)

            elif element == "TextInput":
                form = TextInputElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/TextInput.html', context=context)

            elif element == "EmailInput":
                form = EmailInputElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/EmailInput.html', context=context)

            elif element == "NumberInput":
                form = NumberInputElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/NumberInput.html', context=context)

            elif element == "MultipleChoice":
                form = MultipleChoiceElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/MultipleChoice.html', context=context)
            
            elif element == "SingleChoice":
                form = SingleChoiceElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/SingleChoice.html', context=context)

            elif element == "AgreeDisagree":
                form = AgreeDisagreeElementForm()
                context = {
                    'user_quiz': user_quiz,
                    'quiz_page': quiz_page,
                    'form': form,
                }
                return render(request, 'element_forms/AgreeDisagree.html', context=context)

        return HttpResponse("An error occured")


@login_required
def all_element_swatches(request, quiz_id, page_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():

            context = {
                'user_quiz': user_quiz[0],
                'quiz_page': quiz_page[0],
            }
            return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def add_text_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = TextElementForm(request.POST)
                print(request.POST)
                # If data is valid, proceeds to create a new post
                print("Adding text element")
                print(form.errors)
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    text_element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    text_element.page_element = quiz_page_element
                    text_element.save()

                    # determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)



@login_required
def add_text_input_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = TextInputElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def add_char_input_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = CharInputElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def add_email_input_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = EmailInputElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def add_number_input_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = NumberInputElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def add_multiple_choice_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = MultipleChoiceElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    form = MultipleChoiceChoiceForm()
                    choices = MultipleChoiceChoice.objects.filter(
                        multiple_choice_element=element)

                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                        'element': element,
                        'form': form,
                        'choices': choices,
                    }

                    # Here render the modal ability to add choices
                    return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)



@login_required
def add_single_choice_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = SingleChoiceElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    form = SingleChoiceChoiceForm()
                    choices = SingleChoiceChoice.objects.filter(
                        single_choice_element=element)

                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                        'element': element,
                        'form': form,
                        'choices': choices,
                    }

                    # Here render the modal ability to add choices
                    return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)

@login_required
def add_agree_disagree_element(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
            if request.method == 'POST':
                # Bind data from request.POST into a PostForm
                form = AgreeDisagreeElementForm(request.POST)
                # If data is valid, proceeds to create a new post
                if form.is_valid():
                    quiz_page = quiz_page[0]
                    element = form.save(commit=False)
                    try:
                        position = QuizPageElement.objects.filter(
                            page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(
                        page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    # determine position and create element objects
                    form = AgreeDisagreeRowForm()
                    choices = AgreeDisagreeRow.objects.filter(
                        agree_disagree_element=element)

                    context = {
                        'user_quiz': user_quiz[0],
                        'quiz_page': quiz_page,
                        'element_added': True,
                        'element': element,
                        'form': form,
                        'choices': choices,
                    }

                    # Here render the modal ability to add choices
                    return render(request, 'element_forms/AddRowAgreeDisagreeModal.html', context=context)




@login_required
def move_page_up(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.filter(quiz=user_quiz, id=page_id)
        if quiz_page.exists():
            quiz_page = quiz_page[0]
            quiz_page_before = QuizPage.objects.filter(
                quiz=user_quiz, number__lt=quiz_page.number).order_by('number')
            if quiz_page_before.exists():
                quiz_page_before = quiz_page_before.last()
                quiz_page_number = quiz_page.number
                quiz_page.number = quiz_page_before.number
                quiz_page.save()
                quiz_page_before.number = quiz_page_number
                quiz_page_before.save()

    quiz_pages = QuizPage.objects.filter(quiz=user_quiz).order_by('number')
    context = {
        'user_quiz': user_quiz,
        'quiz_pages': quiz_pages,

    }

    return render(request, 'questions_page.html', context=context)


@login_required
def move_page_down(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.filter(quiz=user_quiz, id=page_id)
        if quiz_page.exists():
            quiz_page = quiz_page[0]
            quiz_page_after = QuizPage.objects.filter(
                quiz=user_quiz, number__gt=quiz_page.number).order_by('number')
            if quiz_page_after.exists():
                quiz_page_after = quiz_page_after.first()
                quiz_page_number = quiz_page.number
                quiz_page.number = quiz_page_after.number
                quiz_page.save()
                quiz_page_after.number = quiz_page_number
                quiz_page_after.save()

    quiz_pages = QuizPage.objects.filter(quiz=user_quiz).order_by('number')
    context = {
        'user_quiz': user_quiz,
        'quiz_pages': quiz_pages,

    }

    return render(request, 'questions_page.html', context=context)


@login_required
def delete_quiz_page(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        quiz_page_number = quiz_page.number
        quiz_pages = QuizPage.objects.filter(
            quiz=user_quiz, number__gt=quiz_page_number)

        quiz_page.delete()
        for page in quiz_pages:
            page_number = page.number
            page.number = page_number - 1
            page.save()

    quiz_pages = QuizPage.objects.filter(quiz=user_quiz).order_by('number')

    context = {
        'user_quiz': user_quiz,
        'quiz_pages': quiz_pages,

    }

    return render(request, 'questions_page.html', context=context)


@login_required
def get_quiz_page_elements(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)

    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)

        quiz_page_elements = quiz_page.get_quiz_page_elements()
        quiz_page_elements = [element.get_element_type()
                              for element in quiz_page_elements]

        elements_count = (len(quiz_page_elements))

        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'quiz_page_elements': quiz_page_elements,
            'elements_count': elements_count,
        }

        try:
            edit = request.GET['edit']
            if edit:
                context['edit'] = True
        except:
            pass

        

        return render(request, 'quiz_page_elements.html', context=context)

    return HttpResponse("An error occured")


@login_required
def delete_page_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(
            page__quiz=user_quiz, id=element_id)
        elements_to_move_up = QuizPageElement.objects.filter(
            page__quiz=user_quiz, position__gt=quiz_page_element.position).order_by('-position')
        quiz_page_element.delete()
        if elements_to_move_up.exists():
            for i in elements_to_move_up:
                i.position -= 1
                i.save()
        return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse("An error occured")


@login_required
def move_element_up(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(
            page__quiz=user_quiz, id=element_id)
        quiz_page_element_before = QuizPageElement.objects.filter(
            page=quiz_page_element.page, position__lt=quiz_page_element.position).order_by('position')
        if quiz_page_element_before.exists():
            quiz_page_element_before = quiz_page_element_before.last()
            element_number = quiz_page_element.position
            element_before_number = quiz_page_element_before.position

            quiz_page_element.position = element_before_number
            quiz_page_element.save()
            quiz_page_element_before.position = element_number
            quiz_page_element_before.save()
        return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse("An error occured")


@login_required
def move_element_down(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(
            page__quiz=user_quiz, id=element_id)
        quiz_page_element_after = QuizPageElement.objects.filter(
            page=quiz_page_element.page, position__gt=quiz_page_element.position).order_by('position')
        if quiz_page_element_after.exists():
            quiz_page_element_after = quiz_page_element_after.first()
            element_number = quiz_page_element.position
            element_before_number = quiz_page_element_after.position

            quiz_page_element.position = element_before_number
            quiz_page_element.save()
            quiz_page_element_after.position = element_number
            quiz_page_element_after.save()
        return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse("An error occured")


@login_required
def add_choice_to_multiple_choice_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = MultipleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice_name = request.POST['choice_name']

        choice = MultipleChoiceChoice.objects.create(
            multiple_choice_element=element, choice=choice_name)
        choices = MultipleChoiceChoice.objects.filter(
            multiple_choice_element=element)
        form = MultipleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)

@login_required
def add_choice_to_single_choice_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = SingleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice_name = request.POST['choice_name']

        choice = SingleChoiceChoice.objects.create(
            single_choice_element=element, choice=choice_name)
        choices = SingleChoiceChoice.objects.filter(
            single_choice_element=element)
        form = SingleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)

@login_required
def add_row_to_agree_disagree_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = AgreeDisagree.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice_name = request.POST['choice_name']
        try:
            position = AgreeDisagreeRow.objects.filter(
                agree_disagree_element=element).order_by('-position')[0].position
        except IndexError:
            position = 0
        position = position + 1

        choice = AgreeDisagreeRow.objects.create(
            agree_disagree_element=element, title=choice_name, position=position)
        choices = AgreeDisagreeRow.objects.filter(
            agree_disagree_element=element)
        form = AgreeDisagreeRowForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddRowAgreeDisagreeModal.html', context=context)



@login_required
def delete_choice_multiple_choice_element(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = MultipleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = MultipleChoiceChoice.objects.get(
            multiple_choice_element=element, id=choice_id).delete()
        choices = MultipleChoiceChoice.objects.filter(
            multiple_choice_element=element)
        form = MultipleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)

@login_required
def delete_choice_single_choice_element(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = SingleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = SingleChoiceChoice.objects.get(
            single_choice_element=element, id=choice_id).delete()
        choices = SingleChoiceChoice.objects.filter(
            single_choice_element=element)
        form = SingleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)

@login_required
def delete_row_agree_disagree_row(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = AgreeDisagree.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = AgreeDisagreeRow.objects.get(
            agree_disagree_element=element, id=choice_id)
        
        choices_above =  AgreeDisagreeRow.objects.filter(
                agree_disagree_element=element, position__gt=choice.position)
        
        for c in choices_above:
            c.position -= 1
            c.save()
        choice.delete()
        choices = AgreeDisagreeRow.objects.filter(
            agree_disagree_element=element)
        form = AgreeDisagreeRowForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddRowAgreeDisagreeModal.html', context=context)





@login_required
def edit_element_title(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)

        element = QuizPageElement.objects.get(
            id=element_id, page__quiz=user_quiz).get_element_type()
        element_type = QuizPageElement.objects.get(
            id=element_id, page__quiz=user_quiz).get_element_type()['type']
        element = element['element']

        element.title = request.POST['title']
        element.save()

        quiz_page_elements = quiz_page.get_quiz_page_elements()
        quiz_page_elements = [element.get_element_type()
                              for element in quiz_page_elements]

        elements_count = (len(quiz_page_elements))
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'quiz_page_elements': quiz_page_elements,
            'elements_count': elements_count,
        }

        if  element_type == "Multiple choice question":
            context['element'] = element
            context['choices'] = MultipleChoiceChoice.objects.filter(
                multiple_choice_element=element)
            context['edit'] = True
            return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)


        elif element_type == "Single choice question":
            context['element'] = element
            context['choices'] = SingleChoiceChoice.objects.filter(
                single_choice_element=element)
            context['edit'] = True
            return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)
        
        elif element_type == "Agree disagree table":
            context['element'] = element
            context['choices'] = AgreeDisagreeRow.objects.filter(
                agree_disagree_element=element)
            context['edit'] = True
            return render(request, 'element_forms/AddRowAgreeDisagreeModal.html', context=context)


        else:
            print("NOT MULTIPLE CHOICE")
            print(element_type)
            return render(request, 'quiz_page_elements.html', context=context)
  
@login_required
def upload_quiz_logo(request, quiz_id):
    print(request)
    print(request.POST)
    images = request.FILES.getlist('logo')

    for image in images:
        if image.size < 2000000 and image.size > 100:
            file_name = image.name
            file_ext = os.path.splitext(file_name)[1]
            if file_ext == '.jpeg':
                file_ext = '.jpg'

            image.name = f"{uuid4()}{file_ext}"
            user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)[0]
            user_quiz.logo = image
            user_quiz.save()

    context = {
        'user_quiz': user_quiz
    }

    return render(request, 'quiz_settings/logo_upload_form.html', context=context)

@login_required
def delete_logo_from_quiz(request, quiz_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)[0]
    user_quiz.logo = None
    user_quiz.save()
    
    context = {
        'user_quiz': user_quiz
    }

    return render(request, 'quiz_settings/logo_upload_form.html', context=context)

@login_required
def update_quiz_analytic_scripts(request, quiz_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)[0]
    user_quiz.analytics_scripts = request.POST['analytics_script']
    user_quiz.save()
    context = {
        'user_quiz': user_quiz,
        'added': True,
    }

    return render(request, 'quiz_settings/analytics_script_form.html', context=context)

@login_required
def get_text_element_edit_form(request, quiz_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)[0]
    element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)

    context = {
        'edit': True,
        'user_quiz': user_quiz,
        'quiz_page': element.page,
        'quiz_page_element': element,
        'form': TextElementForm(instance=element.get_element_type()['element'], prefix=uuid4())
    }

    return render(request, 'element_forms/edit_text_element_page.html', context=context)



# @login_required
# def duplicate_quiz(request, quiz_id):
#     user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)

#     context = {
#         'quiz': user_quiz
#     }

#     return render(request, 'quiz_creation/quizes_list.html', context=context)





@login_required
def upload_image_for_multiple_choice(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = MultipleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = MultipleChoiceChoice.objects.get(id=choice_id, multiple_choice_element=element)

        images = request.FILES.getlist('choice_image')

        for image in images:
            if image.size < 2000000 and image.size > 100:
                file_name = image.name
                file_ext = os.path.splitext(file_name)[1]
                if file_ext == '.jpeg':
                    file_ext = '.jpg'

                image.name = f"{uuid4()}{file_ext}"
                choice.image = image
                choice.save()

        choices = MultipleChoiceChoice.objects.filter(
            multiple_choice_element=element)
        form = MultipleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)

@login_required
def upload_image_for_single_choice(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = SingleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = SingleChoiceChoice.objects.get(id=choice_id, single_choice_element=element)

        images = request.FILES.getlist('choice_image')

        for image in images:
            if image.size < 2000000 and image.size > 100:
                file_name = image.name
                file_ext = os.path.splitext(file_name)[1]
                if file_ext == '.jpeg':
                    file_ext = '.jpg'

                image.name = f"{uuid4()}{file_ext}"
                choice.image = image
                choice.save()

        choices = SingleChoiceChoice.objects.filter(
            single_choice_element=element)
        form = SingleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)
    

@login_required
def mark_as_correct_multiple_choice(request, quiz_id, page_id, element_id, choice_id):
    
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = MultipleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = MultipleChoiceChoice.objects.get(id=choice_id, multiple_choice_element=element)

        try:
            if request.POST['correct']:
                choice.is_correct_choice = True
                choice.save()
        except MultiValueDictKeyError:
                choice.is_correct_choice = False
                choice.save()           

        choices = MultipleChoiceChoice.objects.filter(
            multiple_choice_element=element)
        form = MultipleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)

@login_required
def mark_as_correct_single_choice(request, quiz_id, page_id, element_id, choice_id):
    
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = SingleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = SingleChoiceChoice.objects.get(id=choice_id, single_choice_element=element)
        print(request.POST)
        try:
            if request.POST['correct']:
                choice.is_correct_choice = True
                choice.save()
                
        except MultiValueDictKeyError:
                choice.is_correct_choice = False
                choice.save()           

        choices = SingleChoiceChoice.objects.filter(
            single_choice_element=element)
        form = SingleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)

@login_required
def delete_image_from_multiple_choice(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = MultipleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = MultipleChoiceChoice.objects.get(id=choice_id, multiple_choice_element=element)

        choice.image = None
        choice.save()          

        choices = MultipleChoiceChoice.objects.filter(
            multiple_choice_element=element)
        form = MultipleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceMultipleChoiceModal.html', context=context)
    
@login_required
def delete_image_from_single_choice(request, quiz_id, page_id, element_id, choice_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        element = SingleChoiceElement.objects.get(
            page_element__page=page_id, page_element__page__quiz=quiz_id, id=element_id)

        choice = SingleChoiceChoice.objects.get(id=choice_id, single_choice_element=element)

        choice.image = None
        choice.save()         

        choices = SingleChoiceChoice.objects.filter(
            single_choice_element=element)
        form = SingleChoiceChoiceForm()
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'element_added': False,
            'element': element,
            'form': form,
            'choices': choices,
        }
        # Here render the modal ability to add choices
        return render(request, 'element_forms/AddChoiceSingleChoiceModal.html', context=context)