from django.contrib import admin

from conversion_tracking.models import Pixel

from .models import  Category, Referrer, UserSession
from django.utils.safestring import mark_safe
# Register your models here.




class PixelInline(admin.TabularInline):
    model = Pixel
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PixelInline]

     
class ReferrerInline(admin.TabularInline):
    model = Referrer
    extra = 1

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'time_created', 'user', 'user_agent', 'add_user_agent_to_exclusion_list', 'country_code', 'ip', 'email', 'latest_fbp']
    list_editable = ['add_user_agent_to_exclusion_list']
    inlines = [ReferrerInline]



admin.site.register(Category, CategoryAdmin)

admin.site.register(UserSession, UserSessionAdmin)