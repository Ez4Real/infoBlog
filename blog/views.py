from django.shortcuts import render
from django.conf import settings

from .services.db_services import get_news_by_slug, \
    get_blog_search_results
from .services.blog_services import paginate, \
    check_if_number_endswith_one, add_subscriber_form_to_context, \
    add_last_news_to_context, get_dynamic_page_title_by_language, \
    add_page_title_to_context_by_language
from .services.context_services import get_static_page_context, \
    get_policy_area_context, get_news_type_context, get_media_views_context, \
    get_blog_scholars_page_context
from .services.subscribe_services import get_join_team_form, get_volunteer_form
from .models import Video


def homepage(request, context = {}):
    context['title'] = settings.TITLE    
    add_subscriber_form_to_context(context, request)
    add_last_news_to_context(context)
    
    return render(request, 'blog/homepage.html', context)

def post_detail(request, type, slug, context = {}):
    add_subscriber_form_to_context(context, request)
    context['post'] = post = get_news_by_slug(slug)
    add_page_title_to_context_by_language(
        get_dynamic_page_title_by_language(request, post),
        context
    )
    return render(request, 'blog/post_detail.html', context)

def search(request, context = {}):
    add_page_title_to_context_by_language('Search Results', context)
    add_subscriber_form_to_context(context, request)
    
    if request.method == 'GET':
        query = request.GET.get('search', '')
        results = get_blog_search_results(query)
        
        context['posts_num'] = len_results = str(len(results))
        context['endswith1'] = check_if_number_endswith_one(len_results)
        context['blog_posts'] = paginate(results, request)

    return render(request, 'blog/search.html', context)

'''\About views/'''
def board(request):
    return render(request, 
                  template_name='blog/about/board.html',
                  context=get_static_page_context('Board',
                                                  request)
                  )

def key_doc(request):
    return render(request, 
                  template_name='blog/about/key_doc.html',
                  context=get_static_page_context('Key Documents',
                                                  request)
                  )

def mission(request):
    return render(request, 
                  template_name='blog/about/mission.html',
                  context=get_static_page_context('Mission',
                                                  request)
                  )

def team(request):
    return render(request,
                  template_name='blog/about/team.html',
                  context=get_static_page_context('Team',
                                                   request)
                  )

def profile(request):
    return render(request,
                  template_name='blog/profile/profile.html',
                  context=get_static_page_context('Team',
                                                   request)
                  )

def vision(request):
    return render(request, 
                  template_name='blog/about/vision.html',
                  context=get_static_page_context('Vision',
                                                   request)
                  )

'''\Donate views/'''
def all_donate(request):
    return render(request,
                  template_name='blog/donate/all_donate(old).html',
                  context=get_static_page_context('Donate',
                                                   request)
                  )

'''\Join us views/'''
def general_members(request):
    return render(request,
                  template_name='blog/join_us/general_members.html',
                  context=get_static_page_context('General members',
                                                   request)
                  )

def join_team(request):
    context=get_static_page_context('Join team', request)
    context['join_form'] = get_join_team_form(request)
    return render(request,
                  template_name='blog/join_us/join_team.html',
                  context=context
                  )

def volunteer(request):
    context = get_static_page_context('Volunteering', request)
    context['volunteer_form'] = get_volunteer_form(request)
    return render(request,
                  template_name='blog/join_us/volunteer.html',
                  context=context
                  )

'''\Media views/'''
def podcast(request):
    return render(request, 
                  template_name='blog/media/podcast.html',
                  context=get_media_views_context(Video.MEDIA_CHOICES[0],
                                                  request)
                  )

def videos(request):
    return render(request,
                  template_name='blog/media/videos.html',
                  context=get_media_views_context(Video.MEDIA_CHOICES[1],
                                                  request)
                  )

'''\Policy areas views/'''
def foreign_policy(request):
    return render(request, 
                  template_name='blog/policy_areas/foreign_policy.html', 
                  context=get_policy_area_context('Foreign policy', request)
                  )

def internal_policy(request):
    return render(request, 
                  template_name='blog/policy_areas/internal_policy.html', 
                  context=get_policy_area_context('Internal policy', request)
                  )

def economics(request):
    return render(request, 
                  template_name='blog/policy_areas/economics.html', 
                  context=get_policy_area_context('Economics', request)
                  )


def security(request):
    return render(request, 
                  template_name='blog/policy_areas/security.html',
                  context=get_policy_area_context('Security', request)
                  )

def education(request):
    return render(request,
                  template_name='blog/policy_areas/education.html',
                  context=get_policy_area_context('Education', request)
                  )

def democracy(request):
    return render(request, 
                  template_name='blog/policy_areas/democracy.html',
                  context=get_policy_area_context('Democracy', request)
                  )

def human_rights(request):
    return render(request,
                  template_name='blog/policy_areas/human_rights.html',
                  context=get_policy_area_context('Human rights', request)
                  )

def culture(request):
    return render(request, 
                  template_name='blog/policy_areas/culture.html',
                  context=get_policy_area_context('Culture', request)
                  )


'''\Research views/'''
def analytics(request):
    return render(request,
                  template_name='blog/research/analytics.html',
                  context=get_news_type_context('Analytics',
                                                request)
                  )

def annual_report(request):
    return render(request,
                  template_name='blog/research/annual_report.html',
                  context=get_static_page_context('Annual report',
                                                   request)
                  )


def index_ergosum(request):
    return render(request,
                  template_name='blog/research/index_ergosum.html',
                  context=get_static_page_context('Index ERGOSUM',
                                                   request)
                  )

def opinion(request):
    return render(request,
                  template_name='blog/research/opinion.html',
                  context=get_news_type_context('Opinion', 
                                                request)
                  )


'''\Main views/'''
def blog(request):
    return render(request,
                  template_name='blog/blog.html',
                  context=get_blog_scholars_page_context(request)
                  )

def events(request):
    return render(request,
                  template_name='blog/events.html',
                  context=get_news_type_context('Events',
                                                request)
                  )

def news(request):
    return render(request,
                  template_name='blog/news.html',
                  context=get_news_type_context('News',
                                                request)
                  )

def op_eds(request):
    return render(request,
                  template_name='blog/op_eds.html',
                  context=get_news_type_context('Op-eds',
                                                request)
                  )
