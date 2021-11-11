"""
Factories for testing posts app
"""

import factory
from faker import Faker

fake = Faker()

from apps.posts.models import Comment, Post
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    User Factory is used for creating a user
    """
    class Meta:
        """
        Meta information
        """
        model = User

    username = factory.Faker("name")
    password = "password"
    email = factory.Faker("company_email")


class PostFactory(factory.django.DjangoModelFactory):
    """
    User Factory is used for creating a post
    """
    class Meta:
        """
        Meta information
        """
        model = Post

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    uploaded_file = "/media/uploaded_file.jpg"
    thumbnail_image = "/media/thumbnail_image.jpg"
    owner = factory.SubFactory(UserFactory)
    file_type = 0
    is_private = False


class CommentFactory(factory.django.DjangoModelFactory):
    """
    User Factory is used for creating a comment
    """
    class Meta:
        """
        Meta information
        """
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    comment_text = factory.Faker("sentence")
