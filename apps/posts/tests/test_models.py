"""
Test cases for models in the posts app
"""
from django.test import TestCase

from apps.posts.models import Comment, Post
from apps.users.models import User


class TestPostModel(TestCase):
    """
    Class contains all the test cases written for the Post model
    """

    def setUp(self):
        """
        Setup function creates an object and stores it in database
        for testing
        """
        self.post = Post()
        self.post.title = "title"
        self.post.description = "description"
        self.post.uploaded_file = "uploads/uploaded_file.jpeg"
        self.post.thumbnail_image = "thumbnail_images/image.jpeg"
        self.post.owner = User.objects.create_user(
            username="test_user", password="arbisoft", email="test_user@gmail.com"
        )
        self.post.file_type = "1"
        self.post.is_private = False
        self.post.save()

    def test_post_fields(self):
        """
        Test case checking the fields
        """
        post = Post()
        post.title = "title"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = User.objects.create_user(
            username="test_user2", password="arbisoft", email="test_user@gmail.com"
        )
        post.file_type = "1"
        post.is_private = False
        post.save()

        record = Post.objects.get(pk=post.pk)
        self.assertEqual(record, post)

    def test_get_username(self):
        """
        Test case checking the __str__ function in Post model
        """
        self.assertEqual(self.post.__str__(), "title")


class TestCommentModel(TestCase):
    """
    Class contains all the test cases written for the Comment model
    """

    def test_comment_fields(self):
        """
        Test case checking the fields in the comment model
        """

        user = User.objects.create_user(
            username="test_user2", password="arbisoft", email="test_user@gmail.com"
        )
        user.save()

        post = Post()
        post.title = "title"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = user
        post.file_type = "1"
        post.is_private = False
        post.save()

        comment = Comment()
        comment.comment_text = "comment"
        comment.author = user
        comment.post = post
        comment.save()

        record = Comment.objects.get(pk=comment.pk)
        self.assertEqual(record, comment)
