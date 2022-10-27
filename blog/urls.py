from django.urls import path
from blog import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('delete/<uidb64>/<token>/', views.delete, name='delete'),
    path('activate/<uidb64>/<token>/<lang>/', views.activate, name='activate'),
    path('<type>/<slug:slug>', views.post_detail, name='post-detail'),
    path('search/', views.search, name='search'),
    # About
    path('about/board/', views.board, name='board'),
    path('about/key-docs/', views.key_doc, name='key_documents'),
    path('about/mission/', views.mission, name='mission'),
    path('about/team/', views.team, name='team'),
    path('about/vision/', views.vision, name='vision'),
    # Donate
    path('donate/beav/', views.beav, name='beav'),
    path('donate/patrion/', views.patrion, name='patrion'),
    path('donate/pay-pal/', views.pay_pal, name='pay_pal'),
    path('donate/', views.all_donate, name='all_donate'),
    # Join us
    path('join-us/general-members/', views.general_members, name='general_members'),
    path('join-us/join-team/', views.join_team, name='join_team'),
    path('join-us/voluntear/', views.voluntear, name='voluntear'),
    # Policy areas
    path('policy-areas/foreign-policy/', views.foreign_policy, name='foreign_policy'),
    path('policy-areas/internal-policy/', views.internal_policy, name='internal_policy'),
    path('policy-areas/economics/', views.economics, name='economics'),
    path('policy-areas/security/', views.security, name='security'),
    path('policy-areas/education/', views.education, name='education'),
    path('policy-areas/democracy/', views.democracy, name='democracy'),
    path('policy-areas/human-rights/', views.human_rights, name='human_rights'),
    path('policy-areas/culture/', views.culture, name='culture'),
    # Media
    path('media/podcast/', views.podcast, name='podcast'),
    path('media/videos/', views.videos, name='videos'),
    # Research
    path('research/analytics/', views.analytics, name='analytics'),
    path('research/annual-report/', views.annual_report, name='annual_report'),
    path('research/index-ergosum/', views.index_ergosum, name='index_ergosum'),
    path('research/opinion/', views.opinion, name='opinion'),
    # Else
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('news/', views.news, name='news'),
    path('op_eds/', views.op_eds, name='op_eds'),
]