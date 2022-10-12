from django.urls import path
from blog import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('delete/<uidb64>/<token>', views.delete, name='delete'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('<type>/<slug:slug>/', views.posts, name='post-detail'),
    path('search', views.search, name='search'),
    # About
    path('about/board/', views.board, name='board'),
    path('about/key_doc/', views.key_doc, name='key_documents'),
    path('about/mission/', views.mission, name='mission'),
    path('about/team/', views.team, name='team'),
    path('about/vision/', views.vision, name='vision'),
    # Donate
    path('donate/beav/', views.beav, name='beav'),
    path('donate/patrion/', views.patrion, name='patrion'),
    path('donate/pay_pal/', views.pay_pal, name='pay_pal'),
    path('donate', views.all_donate, name='all_donate'),
    # Join us
    path('join_us/general_members/', views.general_members, name='general_members'),
    path('join_us/join_team/', views.join_team, name='join_team'),
    path('join_us/voluntear/', views.voluntear, name='voluntear'),
    # Media
    path('media/podcast/', views.podcast, name='podcast'),
    path('media/videos/', views.videos, name='videos'),
    # Research
    path('research/analitics', views.analitics, name='analitics'),
    path('research/anual_report', views.anual_report, name='anual_report'),
    path('research/index_ergosum', views.index_ergosum, name='index_ergosum'),
    path('research/opinion', views.opinion, name='opinion'),
    # Else
    path('blog', views.blog, name='blog'),
    path('events', views.events, name='events'),
    path('news', views.news, name='news'),
    path('op_eds', views.op_eds, name='op_eds'),
]