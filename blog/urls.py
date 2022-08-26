from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<uidb64>/<token>', views.delete, name='delete'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]