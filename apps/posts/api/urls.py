"""
URLs in the posts app api
"""
from django.urls import path

from .views import PostCommentAPI, PostSearchAPI

urlpatterns = [
    path("search/", PostSearchAPI, name="post_search"),
    path("comment/", PostCommentAPI, name="post_comment"),
]
