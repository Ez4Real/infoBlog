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
    
    path('library/books/', views.book_list, name='book-list'),
    path('library/<str:type>/', views.cover_list, name='cover-list'),
    path('<type>/<slug:slug>/', views.post_detail, name='post-detail'),
    path('blog/scholar-posts/<slug:slug>/', views.scholar_posts, name='scholar-posts'),
    path('blog/<author_slug>/<slug:slug>/', views.blog_post_detail, name='blog-post-detail'),
    path('about/team/<slug:slug>/', views.team_member_detail, name='team-member-detail'),
    path('search/', views.search, name='search'),
    path("sw.js", views.ServiceWorkerView.as_view(), name="sw.js"),
    
    path('<str:type>/', views.news_type_view, name='news-type'),
    
    # About
    path('about/board', views.board, name='board'),
    path('about/key-docs', views.key_doc, name='key_documents'),
    path('about/mission', views.mission, name='mission'),
    path('about/team', views.team, name='team'),
    path('about/vision', views.vision, name='vision'),
    
    # Library
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('library/', views.library, name='library'),
    path('library/book/<slug:slug>/', views.book_detail, name='book-detail'),
    path('library/author/<slug:slug>/', views.author_book_list, name='author-list'),
    path('library/<str:type>/<slug:slug>/', views.cover_detail, name='cover-detail'),
    
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
    
    path('policy-area/<slug:slug>', views.policy_area, name='policy_area'),
    
    # Media
    path('media/podcast', views.podcast, name='podcast'),
    path('media/videos', views.videos, name='videos'),
    
    # Research
    path('research/annual-report', views.annual_report, name='annual_report'),
    path('research/index-ergosum', views.index_ergosum, name='index_ergosum'),
    
    # Else
    path('blog/', views.blog, name='blog'),
]