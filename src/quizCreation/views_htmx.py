from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import UserQuiz, QuizPage, QuizPageElement, TextElement
from .forms import TextElementForm, CharInputElementForm, TextInputElementForm

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
def quiz_page_element_add(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.filter(quiz=user_quiz, id=page_id)
        if quiz_page.exists():
            quiz_page = quiz_page[0]
        #don't create the object yet just determine which element the user selected
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
                        position = QuizPageElement.objects.filter(page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(page=quiz_page, position=position)
                    text_element.page_element = quiz_page_element
                    text_element.save()
                    

                    #determine position and create element objects
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
                        position = QuizPageElement.objects.filter(page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    #determine position and create element objects
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
                        position = QuizPageElement.objects.filter(page=quiz_page).order_by('-position')[0].position
                    except IndexError:
                        position = 0
                    position = position + 1
                    quiz_page_element = QuizPageElement.objects.create(page=quiz_page, position=position)
                    element.page_element = quiz_page_element
                    element.save()
                    #determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0], 
                        'quiz_page': quiz_page,
                        'element_added': True,
                    }
                    return render(request, 'element_forms/all_elements_swatches.html', context=context)


@login_required
def move_page_up(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.filter(quiz=user_quiz, id=page_id)
        if quiz_page.exists():
            quiz_page = quiz_page[0]
            quiz_page_before  = QuizPage.objects.filter(quiz=user_quiz, number__lt=quiz_page.number).order_by('number')
            if quiz_page_before.exists():
                quiz_page_before = quiz_page_before[0]
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
            quiz_page_after  = QuizPage.objects.filter(quiz=user_quiz, number__gt=quiz_page.number).order_by('number')
            if quiz_page_after.exists():
                quiz_page_after = quiz_page_after[0]
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
        quiz_pages = QuizPage.objects.filter(quiz=user_quiz, number__gt=quiz_page_number)

        quiz_page.delete()
        for page in quiz_pages:
            page_number  = page.number
            page.number = page_number -1
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
        quiz_page_elements = [element.get_element_type() for element in quiz_page_elements]
        
        elements_count = (len(quiz_page_elements))

        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'quiz_page_elements': quiz_page_elements,
            'elements_count': elements_count,
        }

        return render(request, 'quiz_page_elements.html', context=context)

    return HttpResponse("An error occured")

@login_required
def delete_page_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id).delete()
        return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse("An error occured")

@login_required
def move_element_up(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        quiz_page_element_before = QuizPageElement.objects.filter(page=quiz_page_element.page, position__lt=quiz_page_element.position).order_by('position')
        if quiz_page_element_before.exists():
            quiz_page_element_before = quiz_page_element_before[0]
            element_number  = quiz_page_element.position
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
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        quiz_page_element_after = QuizPageElement.objects.filter(page=quiz_page_element.page, position__gt=quiz_page_element.position).order_by('position')
        if quiz_page_element_after.exists():
            quiz_page_element_after = quiz_page_element_after[0]
            element_number  = quiz_page_element.position
            element_before_number = quiz_page_element_after.position

            quiz_page_element.position = element_before_number
            quiz_page_element.save()
            quiz_page_element_after.position = element_number
            quiz_page_element_after.save()
        return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse("An error occured")


@login_required
def edit_element_modal(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        element = quiz_page_element.get_element_type()
        element_type = element['type']
        if element_type == 'Text element':
            text_element = element['element']
            form = TextElementForm(initial={'content': text_element.content})

            context = {
                'user_quiz': user_quiz,
                'quiz_page': quiz_page_element.page,
                'quiz_page_element': quiz_page_element,
                'form': form,
                'edit': True,
            }
            return render(request, 'element_forms/text.html', context=context)




@login_required
def edit_text_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        element = quiz_page_element.get_element_type()
        element_type = element['type']
        text_element = element['element']
        form = TextElementForm(request.POST, instance=text_element)

        if form.is_valid():
            form.save()

            return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)
    return HttpResponse(500, content="An error occured")

@login_required
def edit_text_input_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        element = quiz_page_element.get_element_type()
        element_type = element['type']
        text_element = element['element']
        form = TextInputElementForm(request.POST, instance=text_element)

        if form.is_valid():
            form.save()
            return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)    
    return HttpResponse(500, content="An error occured")

@login_required
def edit_char_input_element(request, quiz_id, page_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)
        element = quiz_page_element.get_element_type()
        element_type = element['type']
        text_element = element['element']
        form = CharInputElementForm(request.POST, instance=text_element)
        if form.is_valid():
            form.save()
            return redirect('get_quiz_page_elements', quiz_id=quiz_id, page_id=page_id)    
    return HttpResponse(500, content="An error occured")