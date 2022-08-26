import re

from .models import News, Subscriber
from .forms import SubscriberForm
from .tokens import email_activation_token

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect


def activateEmail(request, sub, to_email):
    mail_subject = 'Activate your email newsletter subscription'
    message = render_to_string('blog/email/activate_subscription.html', {
        'user': sub.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(sub.pk)),
        'token': email_activation_token.make_token(sub),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'Email has been added. Please, check your email')
    else:
        messages.error(request, 'Problem sending email to this adress, check if you typed it correctly')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        sub = Subscriber.objects.get(pk=uid)
    except:
        sub = None
    
    if sub is not None and email_activation_token.check_token(sub, token):
        sub.is_active = True
        sub.save()
        messages.success(request, 'Thank you for subscription subscription.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('index')

def delete(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        sub = Subscriber.objects.get(pk=uid)
    except:
        sub = None
    
    if sub is not None and email_activation_token.check_token(sub, token):
        sub.delete()
        messages.success(request, 'Unsubscribed success')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('index')


def index(request):
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    
    form = SubscriberForm()
    
    if request.POST:
        sub = Subscriber(email=request.POST['email'])
        if Subscriber.objects.filter(email=sub.email).exists():
            messages.error(request, 'This address is already subscribed!')
        elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sub.email):
            messages.error(request, 'This address is not valid!')
        else:
            sub.save()
            activateEmail(request, sub, sub.email)
            
    return render(request, 'blog/index.html', 
                    {'last_news':last_news,
                    'last_opeds':last_opeds,
                    'last_analytics':last_analytics,
                    'last_opinions':last_opinions,
                    'form': form, }) 
    
