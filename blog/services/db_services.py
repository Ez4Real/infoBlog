from django.db.models import Q, QuerySet
from ..models import News, Video, BlogScholar


def get_news_by_policy_area(policy_area: str) -> QuerySet:
    """ Returns QuerySet of News by policy_area """
    return News.objects.filter(policy_area__name=policy_area).order_by('-date_of_creation')   

def get_news_by_type(type: str) -> QuerySet:
    """ Returns QuerySet of News by type """
    return News.objects.filter(type__type=type).order_by('-date_of_creation')

def get_videocontent_by_type(type: str) -> QuerySet:
    return Video.objects.filter(type=type).order_by('-date_of_creation')

def get_news_by_slug(slug: str) -> str: 
    """ Returns str object of post by slug """
    return News.objects.get(slug=slug)
    
def get_blog_search_results(query: str) -> QuerySet:
    """ Returns QuerySet of News by query """
    return News.objects.filter(Q(en_title__icontains=query) | Q(uk_title__icontains=query) |
                               Q(en_subtitle__icontains=query) | Q(uk_subtitle__icontains=query) |
                               Q(en_content__icontains=query) | Q(uk_content__icontains=query)
                               ).order_by('-date_of_creation')

def get_all_blog_scholars() -> QuerySet:
    """ Returns QuerySet of all Blog Scholars """
    return BlogScholar().get_all_objects()