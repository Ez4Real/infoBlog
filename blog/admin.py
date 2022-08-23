from django.contrib import admin

from .models import News, NewsType, Subscriber, Video


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
        
send_newsletter.short_description = "Send selected Newsletters to all subscribers"


@admin.register(NewsType)
class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed', 'conf_num')
    fields = [('email', 'confirmed'), 'conf_num']
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'date_of_creation')
    list_filter = ('type', 'date_of_creation')
    fields = [('type', 'date_of_creation'), 'title', 'text']
    actions = [send_newsletter]
    
@admin.register(Video)
class Video(admin.ModelAdmin):
    list_display = ('video',)
