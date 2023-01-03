from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import UserQuiz, QuizPage, QuizPageElement, TextElement
from .forms import TextElementForm

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
        quiz_page = QuizPage.objects.filter(quiz=user_quiz[0], id=page_id)
        if quiz_page.exists():
        #don't create the object yet just determine which element the user selected
        #  and pass the required form
            form = TextElementForm()
            context = {
                'user_quiz': user_quiz[0], 
                'quiz_page': quiz_page[0],
                'form': form,
            }
            

            #get element using request.post
            return render(request, 'element_forms/text.html', context=context)

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
                        position = QuizPageElement.objects.filter(page=quiz_page).order_by('position')[0].position
                    except IndexError:
                        position = 0
                    quiz_page_element = QuizPageElement.objects.create(page=quiz_page, position=position+1)
                    text_element.page_element = quiz_page_element
                    text_element.save()
                    

                    #determine position and create element objects
                    context = {
                        'user_quiz': user_quiz[0], 
                        'quiz_page': quiz_page,
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