from django.contrib import admin

from .models import NewsType, PolicyArea, News, Subscriber, Video, \
    BlogScholar, Blog, TeamMember


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
    list_display = ('email', 'is_active', 'mailing_language')
    fields = [('email', 'is_active'), 'mailing_language']
    
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('en_full_name', 'uk_full_name', 'en_position', 'uk_position')
    list_filter = ('en_full_name', 'uk_full_name', 'en_position', 'uk_position')
    fields = [('image',), 
              ('en_full_name', 'uk_full_name'),
              ('en_position', 'uk_position'),
              ('en_content', 'uk_content')]
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'uk_title', 'type', 'policy_area', 'author', 'date_of_creation')
    list_filter = ('type', 'policy_area', 'author', 'en_title', 'uk_title', 'date_of_creation')
    fields = [('type', 'policy_area', 'banner'), 
              ('en_title', 'uk_title', 'author'),
              ('en_subtitle', 'uk_subtitle'),
              ('en_content', 'uk_content')]
    actions = [send_newsletter]
    
@admin.register(BlogScholar)
class BlogScholarAdmin(admin.ModelAdmin):
    list_display = ('en_full_name', 'uk_full_name', 'en_position', 'uk_position')
    list_filter = ('en_full_name', 'uk_full_name', 'en_position', 'uk_position')
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
