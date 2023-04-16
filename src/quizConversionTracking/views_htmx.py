from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from .models import Pixel

@login_required
def add_fb_tiktok_capi(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    context = {
        'user_quiz': user_quiz
    }

    Pixel.objects.create(quiz=user_quiz, pixel_id=request.POST['pixel_id'],
                          integration_type=str(request.POST['integration_type']).lower(), 
                          conv_api_token=request.POST['conv_api_token']
                          )


    context['conversion_api_pixels'] = Pixel.objects.filter(quiz=user_quiz)

    return render(request, 'quiz_conversion_tracking/conversion_api.html', context=context)


@login_required
def delete_fb_tiktok_capi(request, quiz_id, pixel_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    context = {
        'user_quiz': user_quiz
    }

    Pixel.objects.get(quiz=user_quiz, id=pixel_id).delete()

    context['conversion_api_pixels'] = Pixel.objects.filter(quiz=user_quiz)

    return render(request, 'quiz_conversion_tracking/conversion_api.html', context=context)