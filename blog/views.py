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
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .forms import SubscriberForm
from .models import News, Subscriber, Video
from .tokens import email_activation_token



POSTS_PER_PAGE = 15
UK_TITLE = 'Європейська Дослідницька Група Підтримки Членства України – ERGOSUM'
EN_TITLE = 'European Research Group Of Support for Ukrainian Membership – ERGOSUM'


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
    match request.LANGUAGE_CODE:
            case 'en':
                context['title'] = ' | '.join(('Search results', EN_TITLE))
            case 'uk':
                context['title'] = ' | '.join(('Результати пошуку', UK_TITLE))
    context['form'] = subscribeForm(request)
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
        context['endswith1'] = True if context['posts_num'].endswith('1') and context['posts_num'] != '11' else False
        context['blog_posts'] = paginate(results, request, context)

    return render(request, 'blog/search.html', context)


def homepage(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = 'ERGOSUM – European Research Group Of Support for Ukrainian Membership'
        case 'uk':
            context['title'] = 'ERGOSUM – Європейська Дослідницька Група Підтримки Членства України'
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


def post_detail(request, type, slug):
    context = {}
    context['form'] = subscribeForm(request)
    try:
        post = News.objects.get(slug=slug)
        context['news'] = post
        match request.LANGUAGE_CODE:
            case 'en':
                context['title'] = ' | '.join((post.en_title, EN_TITLE))
            case 'uk':
                context['title'] = ' | '.join((post.uk_title, UK_TITLE))

    except News.DoesNotExist:
        raise Http404('News does not exist')

    return render(request, 'blog/post_detail.html', context)


"""
________________________________________________________________________________________________________________________
About
"""


def board(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Board | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Дошка | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/about/board.html', context)


def key_doc(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Key Documents | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Ключові документи | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/about/key_doc.html', context)


def mission(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Mission | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Місія | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/about/mission.html', context)


def team(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Team | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Команда | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/about/team.html', context)


def vision(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Vision | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Візія | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/about/vision.html', context)


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
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Podcasts | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Подкасти | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_videos = Video.objects.filter(type='pc').order_by('-date_of_creation')
    context['blog_videos'] = paginate(blog_videos, request, context)
    return render(request, 'blog/media/podcast.html', context)


def videos(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Videos | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Відео | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_videos = Video.objects.filter(type='vd').order_by('-date_of_creation')
    context['blog_videos'] = paginate(blog_videos, request, context)
    return render(request, 'blog/media/videos.html', context)


"""
________________________________________________________________________________________________________________________
Policy Areas
"""
def foreign_policy(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Foreign policy | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Зовнішня політика | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Foreign policy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    
    return render(request, 'blog/policy_areas/foreign_policy.html', context)

def internal_policy(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Internal policy | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Внутрішня політика | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Internal policy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/internal_policy.html', context)

def economics(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Economics | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Економіка | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Economics').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/economics.html', context)

def security(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Security | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Безпека | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Security').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/security.html', context)

def education(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Education | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Освіта | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Education').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/education.html', context)

def democracy(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Democracy | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Демократія | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Democracy').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/democracy.html', context)

def human_rights(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Human rights | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Права людини | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Human rights').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/human_rights.html', context)

def culture(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Culture | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Культура | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(policy_area__name='Culture').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/policy_areas/culture.html', context)

"""
________________________________________________________________________________________________________________________
Research
"""
def analytics(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Analytics | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Аналітика | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Analytics').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/research/analytics.html', context)


def annual_report(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Annual report | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Річний звіт | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/research/annual_report.html', context)


def index_ergosum(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Index ERGOSUM | {EN_TITLE}'
        case 'uk':
            context['title'] = f'ERGOSUM індекс | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/research/index_ergosum.html', context)


def opinion(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Opinion | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Коментарі | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Opinion').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/research/opinion.html', context)


"""
________________________________________________________________________________________________________________________
Main
"""

def blog(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Blog | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Блог | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    return render(request, 'blog/blog.html', context)


def events(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Events | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Події | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Event').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/events.html', context)


def news(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'News | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Новини | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='News').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/news.html', context)


def op_eds(request):
    context = {}
    match request.LANGUAGE_CODE:
        case 'en':
            context['title'] = f'Op-eds | {EN_TITLE}'
        case 'uk':
            context['title'] = f'Статті | {UK_TITLE}'
    context['form'] = subscribeForm(request)
    blog_posts = News.objects.filter(type__type='Op-ed').order_by('-date_of_creation')
    context['blog_posts'] = paginate(blog_posts, request, context)
    return render(request, 'blog/op_eds.html', context)
