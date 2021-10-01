"""
contains all the urls that users app is using
"""

from django.urls import path

from . import views
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "profile/<str:username>/update/",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path("profile/<str:username>/", ProfileDetailView.as_view(), name="profile"),
]
