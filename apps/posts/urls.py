"""
defines all the urls that Posts app is using
"""
from django.urls import path

from .views import (
    PostCreateView,
    PostDashboardView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostSearchView,
    PostUpdateView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path(
        "dashboard/",
        PostDashboardView.as_view(),
        name="dashboard",
    ),
    path("search/", PostSearchView.as_view(), name="post_search"),
    path("file/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "file/<int:pk>/update/",
        PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "file/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="post_delete",
    ),
    path("file/new/", PostCreateView.as_view(), name="post_create"),
]
