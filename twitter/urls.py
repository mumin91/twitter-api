from django.urls import path
from rest_framework.authtoken import views

from twitter.views import *

urlpatterns = [
    path("login/", views.obtain_auth_token, name="login"),
    path("follow/unfollow/", FollowView.as_view(), name="follow_unfollow_user"),
    path("tweet/", TweetView.as_view(), name="tweet"),
    path("me/tweets/", MyTweetsView.as_view(), name="my_tweets"),
    path("me/newsfeed/", NewsfeedView.as_view(), name="newsfeed"),
]
