from django import views
from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('' ,  index  , name="home"),
    # path('register/' , register_attempt , name="register_attempt"),
    # path('login/' , login_attempt , name="login_attempt"),
    # path('token/' , token_send , name="token_send"),
    # path('success/' , success , name='success'),
    # path('verify/<auth_token>' , verify , name="verify"),
    # path('error/' , error_page , name="error"),
    # path('logout/', logout_user, name="logout"),
    # path('post/', post, name="post"),
    path('post/<slug:slug>/', show_post, name='post'),
    path('category/<slug:category_slug>/', get_category, name='category'),
    path('add-news/', add_news, name='add_news'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('add_reply/<int:post_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('profile/', profile, name='user-profile'),
]
