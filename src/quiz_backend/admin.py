from django.contrib import admin

from session_management.models import Referrer

from .models import Answer, Product, Question, QuestionChoice, Quiz, QuizOrder, Response, UserImageUpload
from django.utils.safestring import mark_safe


# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class ResponseAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['id', 'quiz', 'time_added', 'email', 'display_latest_ref', 'last_modified', 'steps_completed', 'completed', 'purchased', 'response_id', 'session', 'user']
    
    def email(self, obj):
        if obj.session.email_obj:
            return obj.session.email_obj.email
        else:
            None
            
    def display_latest_ref(self, obj):
        user_referrers = ""
        referrers = None
        
        if obj.user:
            
            referrers = Referrer.objects.filter(user_session__user=obj.user).order_by('time_created').reverse()

        elif obj.session:
            referrers = Referrer.objects.filter(user_session=obj.session).order_by('time_created').reverse()
        if referrers:
            for ref in referrers:
                user_referrers += f"{ref.referrer} - {ref.audience} - {ref.ad} - <br>{ref.time_created.date()} {ref.time_created.strftime('%I:%M%p')} <br><hr>"
        return mark_safe(user_referrers)
admin.site.register(Response, ResponseAdmin)



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    ordering = ("number",)

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline,]

admin.site.register(Quiz, QuizAdmin)

class QuestionChoiceInline(admin.TabularInline):
    model = QuestionChoice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz',  'title', 'user_preference_type']
    inlines = [QuestionChoiceInline,]

admin.site.register(Question, QuestionAdmin)

class QuizOrderAdmin(admin.ModelAdmin):
    list_display =['timestamp','status', 'order_email', 'order_total', 'currency', 'total_usd' ]

    def order_email(self, obj):
        return obj.email.email
    

admin.site.register(QuizOrder, QuizOrderAdmin)

admin.site.register(Product)

admin.site.register(UserImageUpload)