from django.db.models import Q, QuerySet
from django.utils.safestring import SafeText
from ..models import News, Video, BlogScholar, \
    Blog, TeamMember, LibraryResource


def get_news_by_policy_area(policy_area: str) -> QuerySet:
    """ Returns QuerySet of News by policy_area """
    return News.objects.filter(policy_area__name=policy_area).order_by('-date_of_creation')   

def get_news_by_type(type: str) -> QuerySet:
    """ Returns QuerySet of News by type """
    return News.objects.filter(type__type=type).order_by('-date_of_creation')

def get_videocontent_by_type(type: str) -> QuerySet:
    return Video.objects.filter(type=type).order_by('-date_of_creation')

def get_news_by_slug(slug: SafeText) -> QuerySet: 
    """ Returns News object by slug """
    return News.objects.get(slug=slug)

def get_posts_by_author_slug(slug: SafeText) -> QuerySet:
    """ Returns QuerySet of Blog Posts by author """
    return Blog.objects.filter(author__slug=slug)

def get_blog_post_by_slug(slug: SafeText) -> Blog:
    """ Returns Blog object by slug """
    return Blog.objects.get(slug=slug)

def get_all_blog_scholars() -> QuerySet:
    """ Returns QuerySet of all Blog Scholars """
    return BlogScholar().get_all_objects()

def get_all_team_members():
    """ Returns QuerySet of all Team Members """
    return TeamMember().get_all_objects()

def get_member_by_slug(slug: SafeText) -> TeamMember:
    """ Returns Team Member object by slug """
    return TeamMember.objects.get(slug=slug)
    
def get_blog_scholar_by_slug(slug: SafeText) -> BlogScholar:
    """ Returns BlogScholar object by slug """
    return BlogScholar.objects.get(slug=slug)
    
def get_blog_search_results(query: str) -> QuerySet:
    """ Returns QuerySet of News by query """
    return News.objects.filter(Q(en_title__icontains=query) | Q(uk_title__icontains=query) |
                               Q(en_subtitle__icontains=query) | Q(uk_subtitle__icontains=query) |
                               Q(en_content__icontains=query) | Q(uk_content__icontains=query)
                               ).order_by('-date_of_creation')
    
def get_all_library_resources() -> QuerySet:
    """ Returns QuerySet of all LibraryResources """
    return LibraryResource.objects.all()

def get_resource_by_type(type: SafeText) -> QuerySet: 
    """ Returns LibraryResource object by type """
    return LibraryResource.objects.get(type=type)
