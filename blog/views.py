import re

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q

from .forms import SubscriberForm
from .models import News, Subscriber
from .tokens import email_activation_token


def activateEmail(request, sub, to_email):
    mail_subject = 'Activate your email newsletter subscription'
    message = get_template('blog/email/activate_subscription.html').render({
        'user': sub.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(sub.pk)),
        'token': email_activation_token.make_token(sub),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
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
        messages.success(request, 'Thank you for subscription.')
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
        messages.success(request, 'Unsubscribed successfully')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('index')

def subscribeForm(request):
    if request.POST:
        sub = Subscriber(email=request.POST['email'])
        if Subscriber.objects.filter(email=sub.email).exists():
            messages.warning(request, 'This address is already subscribed!')
        elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sub.email):
            messages.error(request, 'This address is not valid!')
        else:
            sub.save()
            activateEmail(request, sub, sub.email)

    return SubscriberForm()

def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        
        results = News.objects.filter(Q(title__icontains=query) | 
                                      Q(text__icontains=query) |
                                      Q(type__type__icontains=query) )
    return render(request, 'blog/search.html',
                  {'query': query,
                   'results': results,
                   'results_num': len(results)})

def index(request):
    last_news = News.objects.filter(type__type='News').order_by('-id')[:5]
    last_opeds = News.objects.filter(type__type='Op-eds').order_by('-id')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-id')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-id')[:3]
    

    return render(request, 'blog/index.html',
                  {'last_news': last_news,
                   'last_opeds': last_opeds,
                   'last_analytics': last_analytics,
                   'last_opinions': last_opinions,
                   'form': subscribeForm(request), })


def posts(request, type, pk):
    try:
        post = News.objects.get(pk=pk)
    except News.DoesNotExist:
        raise Http404('News does not exist')

    return render(request, 'blog/post_detail.html',
                  context={'news': post})


"""
________________________________________________________________________________________________________________________
About
"""


def board(request):
    return render(request, 'blog/about/board.html', {'form': subscribeForm(request)})


def key_doc(request):
    return render(request, 'blog/about/key_doc.html', {'form': subscribeForm(request)})


def mission(request):
    return render(request, 'blog/about/mission.html', {'form': subscribeForm(request)})


def team(request):
    return render(request, 'blog/about/team.html', {'form': subscribeForm(request)})


def vision(request):
    return render(request, 'blog/about/vision.html', {'form': subscribeForm(request)})


"""
________________________________________________________________________________________________________________________
Donate
"""


def beav(request):
    return render(request, 'blog/donate/beav.html', {'form': subscribeForm(request)})


def patrion(request):
    return render(request, 'blog/donate/patrion.html', {'form': subscribeForm(request)})


def pay_pal(request):
    return render(request, 'blog/donate/pay_pal.html', {'form': subscribeForm(request)})


"""
________________________________________________________________________________________________________________________
Join Us
"""


def general_members(request):
    return render(request, 'blog/join_us/general_members.html', {'form': subscribeForm(request)})


def join_team(request):
    return render(request, 'blog/join_us/join_team.html', {'form': subscribeForm(request)})


def voluntear(request):
    return render(request, 'blog/join_us/voluntear.html', {'form': subscribeForm(request)})


"""
________________________________________________________________________________________________________________________
Media
"""


def podcast(request):
    return render(request, 'blog/media/podcast.html', {'form': subscribeForm(request)})


def videos(request):
    return render(request, 'blog/media/videos.html', {'form': subscribeForm(request)})


"""
________________________________________________________________________________________________________________________
Policy Areas
"""

"""
________________________________________________________________________________________________________________________
Research
"""


def analitics(request):
    return render(request, 'blog/research/analitics.html', {'form': subscribeForm(request)})


def anual_report(request):
    return render(request, 'blog/research/anual_report.html', {'form': subscribeForm(request)})


def index_ergosum(request):
    return render(request, 'blog/research/index_ergosum.html', {'form': subscribeForm(request)})


def opinion(request):
    return render(request, 'blog/research/opinion.html', {'form': subscribeForm(request)})


"""
________________________________________________________________________________________________________________________
Main
"""


def blog(request):
    return render(request, 'blog/blog.html', {'form': subscribeForm(request)})


def events(request):
    return render(request, 'blog/events.html', {'form': subscribeForm(request)})


def news(request):
    return render(request, 'blog/news.html', {'form': subscribeForm(request)})


def op_eds(request):
    return render(request, 'blog/op_eds.html', {'form': subscribeForm(request)})
