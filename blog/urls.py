from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('confirm/', views.confirm, name='confirm'),
]