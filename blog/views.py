from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.safestring import SafeText
from django.views.generic import TemplateView

from .services.db_services import get_news_by_slug, get_blog_scholar_by_slug, \
    get_blog_search_results, get_posts_by_author_slug, get_blog_post_by_slug, \
    get_member_by_slug, get_all_library_resources, get_resource_by_type, \
    get_all_library_books, get_libresource_by_slug, get_books_by_author, \
    get_author_by_name, get_resources_by_type
from .services.blog_services import paginate, \
    check_if_number_endswith_one, add_subscriber_form_to_context, \
    add_last_news_to_context, get_dynamic_page_title_by_language, \
    add_page_title_to_context_by_language, apply_resource_filters
from .services.context_services import get_static_page_context, \
    get_policy_area_context, get_news_type_context, get_media_views_context, \
    get_blog_scholars_page_context, get_team_page_context
from .services.subscribe_services import get_join_team_form, get_volunteer_form
from .services.auth import login_user
from .models import Video
from .forms import LibraryMemberForm, LoginForm, ResourcesFilterForm


class ServiceWorkerView(TemplateView):
    template_name = 'utils/sw.js'
    content_type = "application/javascript"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["static_url"] = settings.STATIC_URL
        return context

def homepage(request, context = {}) -> HttpResponse:
    context['title'] = settings.TITLE    
    add_subscriber_form_to_context(context, request)
    add_last_news_to_context(context)
    
    return render(request, 'blog/homepage.html', context)

def post_detail(request, type, slug, context = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['post'] = post = get_news_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           post.en_title,
                                           post.uk_title),
        context
    )
    return render(request, 'blog/post_detail.html', context)

def team_member_detail(request: HttpRequest,
                       slug: SafeText,
                       context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['post'] = post = get_member_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           post.en_full_name,
                                           post.uk_full_name),
        context
    )
    return render(request, 'blog/team_member_detail.html', context)
    
def blog_post_detail(request: HttpRequest,
                     author_slug: SafeText,
                     slug: SafeText,
                     context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['post'] = post = get_blog_post_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           post.en_title,
                                           post.uk_title),
        context
    )
    return render(request, 'blog/blog_post_detail.html', context)

def scholar_posts(request: HttpRequest,
                  slug: SafeText,
                  context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['author'] = get_blog_scholar_by_slug(slug)
    context['blog_posts'] = get_posts_by_author_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           context['author'].en_full_name,
                                           context['author'].uk_full_name),
        context
    )
    return render(request, 'blog/scholar_posts.html', context)

'''\Authentication/Library/'''
def register(request) -> HttpResponse:
    context = get_static_page_context('Register', request)
    if request.method == 'POST':
        form = LibraryMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('library')
        else: 
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {(error)}')
    else:
        form = LibraryMemberForm()
        
    context['library_form'] = form
    return render(request, 'blog/library/register.html', context)

def login_view(request) -> HttpResponse:
    context = get_static_page_context('Login', request)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if login_user(request, email, password):
                return redirect('library')
    else:
        form = LoginForm()
    
    context['login_form'] = form
    
    return render(request, 'blog/library/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('library')

def library(request: HttpRequest) -> HttpResponse:
    context = get_static_page_context('Library', request)
    context['library_resources'] = get_all_library_resources()
    return render(request, 'blog/library/library.html', context)

def book_list(request: HttpRequest) -> HttpResponse:
    context = get_static_page_context('Books', request)
    books = get_all_library_books()
    context['filter_form'] = form = ResourcesFilterForm(request.GET or None)
    
    if form.is_valid():
        books = apply_resource_filters(books, form.cleaned_data)
            
    context['blog_posts'] = paginate(books, request, settings.RES_PER_PAGE)
    return render(request, 'blog/library/books/list.html', context)

def author_book_list(request: HttpRequest,
                     author: str,
                     context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['blog_posts'] = paginate(get_books_by_author(author),
                                     request,
                                     settings.RES_PER_PAGE)
    context['author'] = author = get_author_by_name(author)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           author.en_full_name,
                                           author.uk_full_name),
        context
    )
    return render(request, 'blog/library/books/author_list.html', context)

def book_detail(request: HttpRequest,
                slug: SafeText,
                context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['book'] = book = get_libresource_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           book.en_title,
                                           book.uk_title),
        context
    )
    return render(request, 'blog/library/books/detail.html', context)

def cover_list(request: HttpRequest,
               type: str) -> HttpResponse:
    context = get_static_page_context(type, request)
    covers = get_resources_by_type(type)
    context['filter_form'] = form = ResourcesFilterForm(request.GET or None)
    
    if form.is_valid():
        covers = apply_resource_filters(covers, form.cleaned_data)
            
    context['blog_posts'] = paginate(covers, request, settings.RES_PER_PAGE)
    context['others'] = ("Brochures", "Other papers")
    return render(request, 'blog/library/covers/list.html', context)
    
def cover_detail(request: HttpRequest,
                 type,
                 slug: SafeText,
                 context: dict = {}) -> HttpResponse:
    add_subscriber_form_to_context(context, request)
    context['cover'] = cover = get_libresource_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request,
                                           cover.en_title,
                                           cover.uk_title),
        context
    )
    return render(request, 'blog/library/covers/detail.html', context)

def search(request: HttpRequest, context: dict = {}):
    add_page_title_to_context_by_language('Search Results', context)
    add_subscriber_form_to_context(context, request)
    
    if request.method == 'GET':
        query = request.GET.get('search', '')
        results = get_blog_search_results(query)
        
        context['posts_num'] = len_results = str(len(results))
        context['endswith1'] = check_if_number_endswith_one(len_results)
        context['blog_posts'] = paginate(results, request, settings.POSTS_PER_PAGE)

    return render(request, 'blog/search.html', context)

'''\About views/'''
def board(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/about/board.html',
                  context=get_static_page_context('Board',
                                                  request)
                  )

def key_doc(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/about/key_doc.html',
                  context=get_static_page_context('Key Documents',
                                                  request)
                  )

def mission(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/about/mission.html',
                  context=get_static_page_context('Mission',
                                                  request)
                  )

def team(request) -> HttpResponse:
    return render(request,
                  template_name='blog/about/team.html',
                  context=get_team_page_context(request)
                  )

def profile(request) -> HttpResponse:
    return render(request,
                  template_name='blog/profile/profile.html',
                  context=get_static_page_context('Team',
                                                   request)
                  )

def vision(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/about/vision.html',
                  context=get_static_page_context('Vision',
                                                   request)
                  )

'''\Donate views/'''
def all_donate(request) -> HttpResponse:
    return render(request,
                  template_name='blog/donate/all_donate(old).html',
                  context=get_static_page_context('Donate',
                                                   request)
                  )

'''\Join us views/'''
def general_members(request) -> HttpResponse:
    return render(request,
                  template_name='blog/join_us/general_members.html',
                  context=get_static_page_context('General members',
                                                   request)
                  )

def join_team(request) -> HttpResponse:
    context=get_static_page_context('Join team', request)
    context['join_form'] = get_join_team_form(request)
    return render(request,
                  template_name='blog/join_us/join_team.html',
                  context=context
                  )

def volunteer(request) -> HttpResponse:
    context = get_static_page_context('Volunteering', request)
    context['volunteer_form'] = get_volunteer_form(request)
    return render(request,
                  template_name='blog/join_us/volunteer.html',
                  context=context
                  )

'''\Media views/'''
def podcast(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/media/podcast.html',
                  context=get_media_views_context(Video.MEDIA_CHOICES[0],
                                                  request)
                  )

def videos(request) -> HttpResponse:
    return render(request,
                  template_name='blog/media/videos.html',
                  context=get_media_views_context(Video.MEDIA_CHOICES[1],
                                                  request)
                  )

'''\Policy areas views/'''
def foreign_policy(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/foreign_policy.html', 
                  context=get_policy_area_context('Foreign policy', request)
                  )

def internal_policy(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/internal_policy.html', 
                  context=get_policy_area_context('Internal policy', request)
                  )

def economics(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/economics.html', 
                  context=get_policy_area_context('Economics', request)
                  )


def security(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/security.html',
                  context=get_policy_area_context('Security', request)
                  )

def education(request) -> HttpResponse:
    return render(request,
                  template_name='blog/policy_areas/education.html',
                  context=get_policy_area_context('Education', request)
                  )

def democracy(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/democracy.html',
                  context=get_policy_area_context('Democracy', request)
                  )

def human_rights(request) -> HttpResponse:
    return render(request,
                  template_name='blog/policy_areas/human_rights.html',
                  context=get_policy_area_context('Human rights', request)
                  )

def culture(request) -> HttpResponse:
    return render(request, 
                  template_name='blog/policy_areas/culture.html',
                  context=get_policy_area_context('Culture', request)
                  )


'''\Research views/'''
def analytics(request) -> HttpResponse:
    return render(request,
                  template_name='blog/research/analytics.html',
                  context=get_news_type_context('Analytics',
                                                request)
                  )

def annual_report(request) -> HttpResponse:
    return render(request,
                  template_name='blog/research/annual_report.html',
                  context=get_static_page_context('Annual report',
                                                   request)
                  )


def index_ergosum(request) -> HttpResponse:
    return render(request,
                  template_name='blog/research/index_ergosum.html',
                  context=get_static_page_context('Index ERGOSUM',
                                                   request)
                  )

def opinion(request) -> HttpResponse:
    return render(request,
                  template_name='blog/research/opinion.html',
                  context=get_news_type_context('Opinion', 
                                                request)
                  )


'''\Main views/'''
def blog(request) -> HttpResponse:
    return render(request,
                  template_name='blog/blog.html',
                  context=get_blog_scholars_page_context(request)
                  )

def events(request) -> HttpResponse:
    return render(request,
                  template_name='blog/events.html',
                  context=get_news_type_context('Events',
                                                request)
                  )

def news(request) -> HttpResponse:
    return render(request,
                  template_name='blog/news.html',
                  context=get_news_type_context('News',
                                                request)
                  )

def op_eds(request) -> HttpResponse:
    return render(request,
                  template_name='blog/op_eds.html',
                  context=get_news_type_context('Op-eds',
                                                request)
                  )
