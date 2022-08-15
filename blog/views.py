import random
import re

from django.shortcuts import render
from django.conf import settings

from .models import News, Subscriber
from .forms import SubscriberForm

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def index(request):
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    
    if request.POST:
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        if Subscriber.objects.filter(email=sub.email).exists():
            action = 'already exists!'
        elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sub.email):
            action = 'is not valid'
        else:
            action = 'has been added. Please, check your email'
            sub.save()
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='Thank you for signing up for newsletter! \
                            Please complete the process by \
                            <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                            confirm your subscription</a>.'.format(request.build_absolute_uri(),
                                                                   sub.email,
                                                                   sub.conf_num))
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        return render(request, 'blog/index.html', 
                      {'last_news':last_news,
                       'last_opeds':last_opeds,
                       'last_analytics':last_analytics,
                       'last_opinions':last_opinions,
                       'form': SubscriberForm(),
                       'email': sub.email, 
                       'action': action, })
    else:
        return render(request, 'blog/index.html', 
                      {'last_news':last_news,
                       'last_opeds':last_opeds,
                       'last_analytics':last_analytics,
                       'last_opinions':last_opinions,
                       'form': SubscriberForm(), }) 

def confirm(request):
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    
    sub = Subscriber.objects.get(email=request.GET['email'])
    action = 'has been denied'
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed, action = True, 'has been confirmed'
        sub.save()
    return render(request, 'blog/index.html', 
                    {'last_news':last_news,
                    'last_opeds':last_opeds,
                    'last_analytics':last_analytics,
                    'last_opinions':last_opinions,
                    
                    'form': SubscriberForm(),
                    'email': sub.email, 
                    'action': action})

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)