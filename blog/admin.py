from django.contrib import admin

from .models import News, NewsType, Subscriber, Video


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
        
send_newsletter.short_description = 'Розіслати обрані новини підписникам'


@admin.register(NewsType)
class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    fields = [('email', 'is_active')]
    
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
