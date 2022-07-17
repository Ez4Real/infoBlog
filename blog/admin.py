from django.contrib import admin

from .models import News, NewsType, UserEmail


@admin.register(NewsType)
class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    
@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'date_of_creation')
    list_filter = ('type', 'date_of_creation')
    fields = [('type', 'date_of_creation'), 'title', 'text_content']