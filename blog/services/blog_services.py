from django.core.paginator import Paginator, Page
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.db.models import QuerySet

from .subscribe_services import get_subscriber_form
from .db_services import get_all_team_members, get_news_by_policy_area, \
    get_videocontent_by_type, get_all_blog_scholars, get_news_by_type
from django.conf import settings

def paginate(queryset: QuerySet, request: HttpRequest) -> Page:
    """ Returns Page object of queryset """
    return Paginator(queryset,
                     settings.POSTS_PER_PAGE
                     ).get_page(request.GET.get('page', 1))

def get_dynamic_page_title_by_language(request: HttpRequest, post: str) -> str:
    """ Returns dynamic page title in current language """
    match request.LANGUAGE_CODE:
        case 'en':
            pre_vbar = post.en_title
        case 'uk':
            pre_vbar = post.uk_title
    return format_lazy('{} | {}', pre_vbar, settings.TITLE)

def check_if_number_endswith_one(amount: str) -> bool:
    """ Checks if results number endswith 1  """
    return True if amount.endswith('1') and amount != '11' else False

def add_last_news_to_context(context: dict, 
                             const_tup: tuple = settings.HOMEPAGE_CONTENT
                             ) -> None:
    """ Adds the latest news to context according to HOMEPAGE_CONTENT """
    for tup in const_tup:
        context[tup[2]] = get_news_by_type(tup[1])[:tup[0]]
        
def add_page_title_to_context_by_language(pre_vbar: str, context: dict) -> None:
    """ Adds page title to context in current language """
    context['title'] = format_lazy('{} | {}', _(pre_vbar), settings.TITLE)

def add_subscriber_form_to_context(context: dict, request: HttpRequest) -> None:
    """ Adds subscriber form to context """
    context['form'] = get_subscriber_form(request)
    
def add_posts_by_policy_area_to_context(context: dict,
                                        request: HttpRequest,
                                        policy_area: str) -> None:
    """ Adds paginated blog posts by policy area """
    context['blog_posts'] = paginate(get_news_by_policy_area(policy_area), 
                                     request)
    
def add_videocontent_by_type_to_context(context: dict,
                                        request: HttpRequest,
                                        type: str) -> None:
    """ Adds paginated video posts by type """
    context['blog_videos'] = paginate(get_videocontent_by_type(type), 
                                      request)
    
def add_posts_by_type_to_context(context: dict,
                                 request: HttpRequest,
                                 type: str) -> None:
    """ Adds paginated blog posts by type """
    context['blog_posts'] = paginate(get_news_by_type(type), 
                                     request)
    
def add_blog_scholars_to_context(context: dict) -> None:
    """ Adds Blog Scholars to context """
    context['blog_scholars'] = get_all_blog_scholars()
    
def add_team_members_to_context(context: dict) -> None:
    """ Adds Team Members to context """
    context['team_members'] = get_all_team_members()
    
