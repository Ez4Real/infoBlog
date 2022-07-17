from django.shortcuts import render

from .models import News


def index(request):
    
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    
    return render(
        request, 
        'index.html',
        context={
            'last_news':last_news,
            'last_opeds':last_opeds,
            'last_analytics':last_analytics,
            'last_opinions':last_opinions
            },
    )
