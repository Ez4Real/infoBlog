from django.http import HttpRequest

from .blog_services import add_videocontent_by_type_to_context, \
    add_page_title_to_context_by_language, add_subscriber_form_to_context, \
    add_posts_by_type_to_context, add_posts_by_policy_area_to_context, \
    add_blog_scholars_to_context

def get_static_page_context(page_name: str,
                            request: HttpRequest,
                            context: dict = {},
                            ) -> dict:
    """ Returns context for static pages """
    add_page_title_to_context_by_language(page_name, context)
    add_subscriber_form_to_context(context, request)
    return context

def get_policy_area_context(policy_area: str, 
                            request: HttpRequest,
                            context: dict = {}
                            ) -> dict:
    """ Returns context for policy area pages """
    add_page_title_to_context_by_language(policy_area, context)
    add_subscriber_form_to_context(context, request)
    add_posts_by_policy_area_to_context(context, request, policy_area)
    return context

def get_media_views_context(media_choices: str,
                            request: HttpRequest,
                            context: dict = {}
                            ) -> dict:
    """ Returns context for media pages """
    add_page_title_to_context_by_language(media_choices[1], context)
    add_subscriber_form_to_context(context, request)
    add_videocontent_by_type_to_context(context, request, media_choices[0])
    return context

def get_news_type_context(type: str,
                          request: HttpRequest,
                          context: dict = {}
                          ) -> dict:
    """ Returns context for news pages of a specific type """
    add_page_title_to_context_by_language(type, context)
    add_subscriber_form_to_context(context, request)
    add_posts_by_type_to_context(context, request, type)
    return context

def get_blog_scholars_page_context(request: HttpRequest
                                  ) -> dict:
    """ Returns context for blog page """
    context = get_static_page_context('Blog', request)
    add_blog_scholars_to_context(context)
    return context