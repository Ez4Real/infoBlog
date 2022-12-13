from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('', include('blog.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
 ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
