"""
Fixtures for post app
"""
import pytest
from pytest_factoryboy import register

from apps.posts.pytest_tests.factories import CommentFactory, PostFactory, UserFactory

register(UserFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture
def user(db, user_factory):
    """
    A simple user is created and returned
    """
    user = user_factory.create()
    return user


@pytest.fixture
def post(db, post_factory):
    """
    A post is created an returned
    """
    post = post_factory.create()
    return post


@pytest.fixture
def comment(db, comment_factory):
    """
    A comment is created and returned
    """
    comment = comment_factory.create()
    return comment


@pytest.fixture
def posts(db, post_factory):
    """
    Ten posts are created and returned
    """
    number_of_posts = 11
    posts = []
    for post_id in range(1, number_of_posts):
        posts.append(post_factory.create(title=f"post {post_id}"))
    return posts


@pytest.fixture
def private_post(db, post_factory):
    """
    A private post is created an returned
    """
    post = post_factory.create(is_private=True)
    return post
