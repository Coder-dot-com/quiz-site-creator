from django.contrib import admin
from .models import *
from session_management.models import Referrer
from django.utils.safestring import mark_safe

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class ResponseAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['id', 'quiz', 'time_added',  'display_latest_ref', 'last_modified', 'steps_completed', 'completed', 'response_id', 'session']
    

            
    def display_latest_ref(self, obj):
        user_referrers = ""
        referrers = None
        
        if obj.session:
            referrers = Referrer.objects.filter(user_session=obj.session).order_by('time_created').reverse()
        if referrers:
            for ref in referrers:
                user_referrers += f"{ref.referrer} - {ref.audience} - {ref.ad} - <br>{ref.time_created.date()} {ref.time_created.strftime('%I:%M%p')} <br><hr>"
        return mark_safe(user_referrers)
    

admin.site.register(Response, ResponseAdmin)