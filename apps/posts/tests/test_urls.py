"""
Module contains all the test cases related to urls in posts app
"""

from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from apps.posts.views import (
    PostCreateView,
    PostDashboardView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)


class TestPostURL(SimpleTestCase):
    """
    Class contains all the test cases written for urls in the posts app
    """

    def test_create_post_url(self):
        """
        Testing case for post_create url
        """
        url = reverse("post_create")
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_dashboard_url(self):
        """
        Testing case for dashboard url
        """
        url = reverse("dashboard")
        self.assertEqual(resolve(url).func.view_class, PostDashboardView)

    def test_home_url(self):
        """
        Testing case for home url
        """
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_update_post_url(self):
        """
        Testing case for post_update url
        """
        url = reverse("post_update", args=["1"])
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)

    def test_delete_post_url(self):
        """
        Testing case for post_delete url
        """
        url = reverse("post_delete", args=["1"])
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)

    def test_detail_post_url(self):
        """
        Testing case for post_detail url
        """
        url = reverse("post_detail", args=["1"])
        self.assertEqual(resolve(url).func.view_class, PostDetailView)
