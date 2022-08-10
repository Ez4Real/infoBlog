from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserEmailForm
from .models import News, UserEmail


def index(request):
    
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    
    save_email(request)
    
    return render(request, 'blog/index.html',
                  {
                  'last_news':last_news,
                  'last_opeds':last_opeds,
                  'last_analytics':last_analytics,
                  'last_opinions':last_opinions,
                  'form': UserEmailForm
                  },
    )
    
def save_email(request):
    form = UserEmailForm(request.POST)
    if request.POST:
        print(form.email)
        if form.is_valid():
            if UserEmail.objects.filter(email=form.email).exists():
                return HttpResponse('The email already exists!')
            else: form.save()
        return redirect(index)  
