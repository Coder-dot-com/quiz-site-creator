from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserQuiz, QuizPage, QuizPageElement
from .forms import TextElementForm, QuizConfirmationForm
from django.shortcuts import redirect

# Create your views here.
@login_required
def create_quiz(request):
    return render(request, 'create_quiz.html')

@login_required
def quiz_edit(request, quiz_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)

    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_pages = QuizPage.objects.filter(quiz=user_quiz).order_by('number')
        context = {
            'user_quiz': user_quiz, 
            'quiz_pages': quiz_pages,

        }
        return render(request, 'quiz_edit.html', context=context)

    return redirect('dashboard_home')

@login_required
def edit_quiz_completion_page(request, quiz_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)

    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_pages = QuizPage.objects.filter(quiz=user_quiz).order_by('number')
        context = {
            'user_quiz': user_quiz, 
            'quiz_pages': quiz_pages,
            'form': QuizConfirmationForm(instance=user_quiz)

        }   
    return render(request, 'quiz_completion_page.html', context=context)

@login_required
def quiz_page_add(request, quiz_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page_number = QuizPage.objects.filter(quiz=user_quiz).order_by('-number')
        if quiz_page_number.exists():
            quiz_page_number = quiz_page_number[0].number
        else:
            quiz_page_number = 0
        quiz_page =  QuizPage.objects.create(quiz=user_quiz, number=(quiz_page_number+1), title=request.POST['name'])
        quiz_page_elements = quiz_page.get_quiz_page_elements()
        print('quiz_page_elements', quiz_page_elements)
        quiz_page_elements = [element.get_element_type() for element in quiz_page_elements]


        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'quiz_page_elements': quiz_page_elements,
        }
        return redirect('quiz_page_edit', quiz_id=user_quiz.id, page_id=quiz_page.id)

    return redirect('dashboard_home')


@login_required
def quiz_page_edit(request, quiz_id, page_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        quiz_page = QuizPage.objects.get(quiz=user_quiz, id=page_id)

        quiz_page_elements = quiz_page.get_quiz_page_elements()
        print('quiz_page_elements', quiz_page_elements)
        quiz_page_elements = [element.get_element_type() for element in quiz_page_elements]

        elements_count = (len(quiz_page_elements))

        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page,
            'quiz_page_elements': quiz_page_elements,
            'elements_count': elements_count,
        }

        return render(request, 'quiz_page_edit.html', context=context)

    return redirect('dashboard_home')

@login_required
def edit_text_element(request, quiz_id, element_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)[0]
    element = QuizPageElement.objects.get(page__quiz=user_quiz, id=element_id)

    print(request.POST)
    for key,value in request.POST.items():
        if key == "csrfmiddlewaretoken":
            pass
        else:
            content = request.POST[key]
            textelement = element.get_element_type()['element']
            textelement.content = content
            textelement.save()

    return quiz_page_edit(request, quiz_id=quiz_id, page_id=element.page.id)