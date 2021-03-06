from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('login_redirect/', views.profile_new, name='login_redirect'),
    path('explore/', views.explore, name='explore'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('profile/<slug:username>/follow', views.follow, name='follow'),
    path('profile/<slug:username>/unfollow', views.unfollow, name='unfollow'),
    path('profile/<slug:username>/subscribe', views.subscribe, name='subscribe'),
    path('profile/<slug:username>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('profile/<slug:username>/followers_view', views.followers_view, name='followers_view'),
    path('password_change/', views.password_change, name='password_change'),
    
    path('new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment', views.comment_add, name='comment_add'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='codebase/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)