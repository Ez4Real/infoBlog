from django.db.models import Q, QuerySet
from django.utils.safestring import SafeText
from ..models import News, Video, BlogScholar, \
    Blog, TeamMember, ResourceType, LibraryResource, \
    LibraryAuthor, PolicyArea


def get_last_news() -> QuerySet:
    """ Returns QuerySet of 5 last News objects """
    return News.objects.order_by('-date_of_creation')[:5]
    
def get_news_by_policy_area(policy_area: str) -> QuerySet:
    """ Returns QuerySet of News by policy_area """
    return News.objects.filter(policy_area__slug=policy_area).order_by('-date_of_creation')

def get_policy_area_by_slug(slug: SafeText) -> str:
    """ Returns PolicyArea object name by slug """
    return PolicyArea.objects.get(slug=slug).name

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
    """ Returns QuerySet of all ResourceTypes """
    return ResourceType.objects.all().reverse()

def get_resource_by_type(type: SafeText) -> QuerySet: 
    """ Returns ResourceType object by type """
    return ResourceType.objects.get(type=type)

def get_all_library_books() -> QuerySet:
    """ Returns all LibraryResources with `Books` type """
    return LibraryResource.objects.filter(type__type='Books').order_by('-date')

def get_books_by_author(author_id: int) -> QuerySet:
    """ Returns LibraryResources with `Books` type by author """
    return get_all_library_books().filter(author=author_id)

def get_libresource_by_slug(slug: SafeText) -> LibraryResource: 
    """ Returns LibraryResource object by slug """
    return LibraryResource.objects.get(slug=slug)

def get_author_by_slug(slug: str) -> LibraryAuthor:
    """ Returns LibraryAuthor object by name """
    return LibraryAuthor.objects.get(slug=slug)

def get_resources_by_type(type: str) -> QuerySet:
    """ Returns LibraryResource objects by type """
    return LibraryResource.objects.filter(type__type=type)