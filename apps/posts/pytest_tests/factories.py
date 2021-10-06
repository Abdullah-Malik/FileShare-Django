import factory
from faker import Faker

fake = Faker()

from apps.posts.models import Comment, Post
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "password"
    email = factory.Faker("company_email")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    uploaded_file = "/media/uploaded_file.jpg"
    thumbnail_image = "/media/thumbnail_image.jpg"
    owner = factory.SubFactory(UserFactory)
    file_type = 0
    is_private = False


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    comment_text = factory.Faker("sentence")
