from django.contrib import admin
from django.urls import path
from blog import views

# this is the urls
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('add_comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('share/<int:blog_id>/', views.share_blog, name='share_blog'),
    path('logout/', views.user_logout, name='logout'),
]