

from django.shortcuts import render, redirect

from common.util.functions import event_id
from conversion_tracking.tasks import conversion_tracking
from session_management.models import Category
from session_management.views import _session
from blog.models import BlogPage

def home(request):

    context = {
    }

    return render(request, 'home_site2/index.html', context=context)



def robots_txt(request):
    return render(request, 'robots.txt')

# def about(request):
#     return render(request, 'home_site2/pages/about.html')

# def contact(request):
#     return render(request, 'home_site2/pages/contact.html')

def tandc(request):
    return render(request, 'home_site2/pages/tandc.html')


def privpolicy(request):
    context = {
    }
    return render(request, 'home_site2/pages/privpolicy.html', context=context)

def deliveryinfo(request):
    return render(request, 'home_site2/pages/deliveryinfo.html')


def refundpolicy(request):
    return render(request, 'home_site2/pages/refundpolicy.html')

def pricing(request):
    return render(request, 'home_site2/pages/pricing.html')


def redirect_old_blog(request, slug):
    page = BlogPage.objects.get(slug=slug)
    
    return redirect(page.get_full_url(request=request))
