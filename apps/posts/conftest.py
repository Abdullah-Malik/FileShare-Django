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


@pytest.fixture
def posts(db, post_factory):
    number_of_posts = 10
    posts = []
    for post_id in range(number_of_posts):
        posts.append(post_factory.create(title=f'post {post_id}'))
    return posts


@pytest.fixture
def private_post(db, post_factory):
    post = post_factory.create(is_private=True)
    return post

