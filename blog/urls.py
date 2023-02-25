from django.urls import path
from blog import views
from .services.subscribe_services import \
activate_user_subscription, deactivate_user_subscription

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('deactivate/<uidb64>/<token>/',
         deactivate_user_subscription,
         name='delete'),
    path('activate/<uidb64>/<token>/<lang>/',
         activate_user_subscription,
         name='activate'),
    path('<type>/<slug:slug>/', views.post_detail, name='post-detail'),
    path('blog/scholar-posts/<slug:slug>/', views.scholar_posts, name='scholar-posts'),
    path('blog/<author_slug>/<slug:slug>/', views.blog_post_detail, name='blog-post-detail'),
    path('about/team/<slug:slug>/', views.team_member_detail, name='team-member-detail'),
    path('search/', views.search, name='search'),
    
    # About
    path('about/board', views.board, name='board'),
    path('about/key-docs', views.key_doc, name='key_documents'),
    path('about/mission', views.mission, name='mission'),
    path('about/team', views.team, name='team'),
    path('about/vision', views.vision, name='vision'),
    
    # Library
    path('library/', views.library, name='library'),
    
    # Donate
    path('donate/', views.all_donate, name='all_donate'),
    
    # Join us
    path('join-us/general-members',
         views.general_members,
         name='general_members'),
    path('join-us/join-team',
         views.join_team,
         name='join_team'),
    path('join-us/volunteer',
         views.volunteer,
         name='volunteer'),
    
    # Policy areas
    path('policy-areas/foreign-policy',
         views.foreign_policy,
         name='foreign_policy'),
    path('policy-areas/internal-policy',
         views.internal_policy,
         name='internal_policy'),
    path('policy-areas/economics', views.economics, name='economics'),
    path('policy-areas/security', views.security, name='security'),
    path('policy-areas/education', views.education, name='education'),
    path('policy-areas/democracy', views.democracy, name='democracy'),
    path('policy-areas/human-rights', views.human_rights, name='human_rights'),
    path('policy-areas/culture', views.culture, name='culture'),
    
    # Media
    path('media/podcast', views.podcast, name='podcast'),
    path('media/videos', views.videos, name='videos'),
    
    # Research
    path('research/analytics', views.analytics, name='analytics'),
    path('research/annual-report', views.annual_report, name='annual_report'),
    path('research/index-ergosum', views.index_ergosum, name='index_ergosum'),
    path('research/opinion', views.opinion, name='opinion'),
    
    # Else
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('news/', views.news, name='news'),
    path('op_eds/', views.op_eds, name='op_eds'),
]