"""
Unit Tests for APIs
"""

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.posts.models import Comment, Post
from apps.users.models import User


class PostAPITests(APITestCase):
    """
    Class contains unit tests for posts app
    """

    def setUp(self):
        """
        setUp runs before each unit test is run
        """
        self.username = "test_user"
        self.password = "arbisoft"

        self.user = User.objects.create_user(
            username=self.username, password=self.password, email="test_user@gmail.com"
        )

        self.post = Post()
        self.post.title = "title1"
        self.post.description = "description"
        self.post.uploaded_file = "uploads/uploaded_file.jpeg"
        self.post.thumbnail_image = "thumbnail_images/image.jpeg"
        self.post.owner = self.user
        self.post.file_type = "1"
        self.post.is_private = False
        self.post.save()

    def test_search_api(self):
        """
        Testing Search Functionality
        """

        url = reverse("post_search")
        query_data = {"q": "title"}
        response = self.client.get(url, query_data, format="json")
        post_data = json.loads(response.content)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_data["title"], self.post.title)

    def test_comment_api(self):

        url = reverse("post_comment")
        comment_post_data = {
            "comment_text": "this is a comment",
            "post": self.post.id,
            "author": self.user.id,
        }
        response = self.client.post(url, comment_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
