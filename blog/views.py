import re

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q

from .forms import SubscriberForm
from .models import News, Subscriber
from .tokens import email_activation_token


POSTS_PER_PAGE = 15


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


def activate(request, uidb64, token, lang):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        sub = Subscriber.objects.get(pk=uid)
    except:
        sub = None

    if sub is not None and email_activation_token.check_token(sub, token):
        sub.is_active = True
        sub.mailing_language = lang
        sub.save()
        messages.success(request, 'Thank you for subscription.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('homepage')


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
    return redirect('homepage')


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


def paginate(queryset, request, context):
    page = request.GET.get('page', 1)
    context['page_num'] = page
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return results


def search(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('search', '')
        context['query'] = str(query)

        results = News.objects.filter(Q(en_title__icontains=query) |
                                      Q(uk_title__icontains=query) |
                                      Q(en_subtitle__icontains=query) |
                                      Q(uk_subtitle__icontains=query) |
                                      Q(en_content__icontains=query) |
                                      Q(uk_content__icontains=query) |
                                      Q(type__type__icontains=query)).order_by('-date_of_creation')
        context['posts_num'] = str(len(results))
        context['endswith1'] = True if context['posts_num'][-1] == '1' and context['posts_num'] != '11' else False
        page = request.GET.get('page', 1)
        context['page_num'] = page
        paginator = Paginator(results, POSTS_PER_PAGE)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(POSTS_PER_PAGE)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context['blog_posts'] = results
    context['form'] = subscribeForm(request)

    return render(request, 'blog/search.html', context)


def homepage(request):
    context = {}
    context['form'] = subscribeForm(request)
    last_news = News.objects.filter(type__type='News').order_by('-date_of_creation')[:5]
    last_opeds = News.objects.filter(type__type='Op-ed').order_by('-date_of_creation')[:3]
    last_analytics = News.objects.filter(type__type='Analytics').order_by('-date_of_creation')[:3]
    last_opinions = News.objects.filter(type__type='Opinion').order_by('-date_of_creation')[:3]
    context['last_news'] = last_news
    context['last_opeds'] = last_opeds
    context['last_analytics'] = last_analytics
    context['last_opinions'] = last_opinions

    return render(request, 'blog/homepage.html', context)


def posts(request, type, slug):
    try:
        post = News.objects.get(slug=slug)
    except News.DoesNotExist:
        raise Http404('News does not exist')

    return render(request, 'blog/post_detail.html',
                  context={'news': post, 'form': subscribeForm(request)})


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


def all_donate(request):
    return render(request, 'blog/donate/all_donate.html', {'form': subscribeForm(request)})


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
def foreign_policy(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Foreign policy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/foreign_policy.html', context)

def internal_policy(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Internal policy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/internal_policy.html', context)

def economics(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Economics').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/economics.html', context)

def security(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Security').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/security.html', context)

def education(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Education').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/education.html', context)

def democracy(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Democracy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/democracy.html', context)

def human_rights(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Human rights').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/human_rights.html', context)

def culture(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Culture').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/culture.html', context)

"""
________________________________________________________________________________________________________________________
Research
"""
def analytics(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Analytics').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/research/analytics.html', context)


def anual_report(request):
    context = {}
    context['form'] = subscribeForm(request)
    return render(request, 'blog/research/anual_report.html', {'form': subscribeForm(request)})


def index_ergosum(request):
    return render(request, 'blog/research/index_ergosum.html', {'form': subscribeForm(request)})


def opinion(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Opinion').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/research/opinion.html', context)


"""
________________________________________________________________________________________________________________________
Main
"""

def blog(request):
    return render(request, 'blog/blog.html', {'form': subscribeForm(request)})


def events(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Event').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/events.html', context)


def news(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='News').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/news.html', context)


def op_eds(request):
    context = {}
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Op-ed').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/op_eds.html', context)
