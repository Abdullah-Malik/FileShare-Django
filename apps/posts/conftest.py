import pytest
from pytest_factoryboy import register

from apps.posts.pytest_tests.factories import CommentFactory, PostFactory, UserFactory

register(UserFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture
def user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def post(db, post_factory):
    post = post_factory.create()
    return post


@pytest.fixture
def comment(db, comment_factory):
    comment = comment_factory.create()
    return comment
