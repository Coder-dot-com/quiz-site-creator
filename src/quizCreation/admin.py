from django.contrib import admin
from .models import UserQuiz, QuizPageElement, QuizPage, TextElement
# Register your models here.

admin.site.register(UserQuiz)


admin.site.register(QuizPage)
admin.site.register(QuizPageElement)
admin.site.register(TextElement)