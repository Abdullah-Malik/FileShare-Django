"""
URLs in the posts app api
"""
from django.urls import path

from .views import PostCommentList, post_comment_api, post_search_api

urlpatterns = [
    path("search/", post_search_api, name="post_search"),
    path("comment/", post_comment_api, name="post_comment"),
    path("comment/list/", PostCommentList.as_view(), name="post_comment_list"),
]
