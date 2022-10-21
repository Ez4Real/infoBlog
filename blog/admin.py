from django.contrib import admin

from .models import News, NewsType, Subscriber, Video


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
        
send_newsletter.short_description = 'Send newsletter to subscribers'


@admin.register(NewsType)
class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    fields = ('type',)
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'mailing_language')
    fields = [('email', 'is_active'), 'mailing_language']
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'uk_title', 'type', 'date_of_creation')
    list_filter = ('type', 'en_title', 'uk_title', 'date_of_creation')
    fields = [('type', 'banner'), 
              ('en_title', 'uk_title'),
              ('en_subtitle', 'uk_subtitle'),
              ('en_content', 'uk_content')]
    actions = [send_newsletter]
    
@admin.register(Video)
class Video(admin.ModelAdmin):
    list_display = ('date_of_creation', 'video')
