from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import NewsType, PolicyArea, News, Subscriber, Video, \
    BlogScholar, Blog, TeamMember, LibraryMember, ResourceType, \
    Subresource, LibraryResource, LibraryAuthor, GeneralMember


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

        
send_newsletter.short_description = 'Send newsletter to subscribers'


@admin.register(NewsType)
class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    fields = ('type',)
    
@admin.register(PolicyArea)
class PolicyAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ('email', 'is_active', 'mailing_language')
    fields = [('email', 'is_active'), 'mailing_language']
    readonly_fields = ['email']
    
@admin.register(TeamMember)
class TeamMemberAdmin(OrderedModelAdmin):
    list_display = ('en_full_name', 'move_up_down_links', 'en_position')
    list_filter = ('date_of_creation', 'en_full_name', 'uk_full_name', 'en_position', 'uk_position')
    fields = [('en_full_name', 'uk_full_name'),
              ('image', 'email'),
              ('en_position', 'uk_position'),
              ('en_content', 'uk_content')]

@admin.register(LibraryMember)
class LibraryMemberAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    
    list_display = ('last_name', 'first_name', 'education_level', 'institution')
    list_filter = ('last_name', 'first_name', 'education_level', 'institution', 'date_of_creation')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number',
                       'education_level', 'institution', 'department', 'specialization',
                       'supervisor', 'google_scholar', 'resource_plans', 'date_of_creation')
    fields = [('first_name', 'last_name'), 
              ('email', 'phone_number'),
              ('education_level', 'institution'),
              ('department'),
              ('specialization_code', 'specialization'),
              ('supervisor', 'google_scholar'),
              ('resource_plans'),
              ('date_of_creation')]
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'uk_title', 'type', 'policy_area', 'author', 'date_of_creation')
    list_filter = ('type', 'date_of_creation', 'en_title', 'uk_title', 'policy_area', 'author')
    fields = [('type', 'policy_area', 'banner'), 
              ('en_title', 'uk_title', 'author'),
              ('en_subtitle', 'uk_subtitle'),
              ('en_content', 'uk_content')]
    actions = [send_newsletter]
    
@admin.register(BlogScholar)
class BlogScholarAdmin(OrderedModelAdmin):
    list_display = ('en_full_name', 'move_up_down_links', 'en_position')
    list_filter = ('date_of_creation', 'en_full_name', 'uk_full_name', 'en_position', 'uk_position')
    fields = [('image',), 
              ('en_full_name', 'uk_full_name'),
              ('en_position', 'uk_position'),
              ('link')]
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'uk_title', 'author', 'date_of_creation')
    list_filter = ('en_title', 'uk_title', 'author', 'date_of_creation')
    fields = [('author'), 
              ('en_title', 'uk_title'),
              ('en_content', 'uk_content')]
    
@admin.register(Video)
class Video(admin.ModelAdmin):
    list_display = ('en_title', 'uk_title', 'date_of_creation')
    list_filter = ('type', 'en_title', 'uk_title', 'date_of_creation')
    
@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('en_name', 'uk_name')
    fields = [('banner'),
              ('en_name', 'uk_name')]

@admin.register(LibraryAuthor)
class LibraryAuthorAdmin(admin.ModelAdmin):
    list_display = ('en_full_name', 'uk_full_name')
    fields = [('en_full_name', 'uk_full_name')]
    
@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'type', 'date')
    fields = [('type', 'banner'),
              ('author', 'pages'),
              ('en_title', 'uk_title'),
              ('en_content', 'uk_content'),
              ('date', 'file')]
    
@admin.register(Subresource)
class SubresourceAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'bounded_resource')
    list_filter = ('topic', 'date', 'bounded_resource')
    fields = [('topic', 'bounded_resource'), 
              ('file', 'date')]
    
@admin.register(GeneralMember)
class GeneralMemberAdmin(OrderedModelAdmin):
    list_display = ('en_name', 'move_up_down_links', 'uk_name')
    list_filter = ('date', 'en_name', 'uk_name')
    fields = [('en_name', 'uk_name'),
              ('banner', 'link'), 
              ('date', 'is_rounded')]