from django.urls import path
from .views import *

urlpatterns = [
    path("welcome/",welcome_page, name="welcome_page"),
    path("profile/", view_profile, name="view_profile"),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/', view_post, name='post_detail'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]