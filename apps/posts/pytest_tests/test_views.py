"""
Tests for views in posts app
"""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.posts.models import Comment, Post
from apps.users.models import User

HOME_URL_NAME = "home"
DASHBOARD_URL_NAME = "dashboard"
POST_CREATE_URL_NAME = "post_create"
POST_UPDATE_URL_NAME = "post_update"
POST_DELETE_URL_NAME = "post_delete"
POST_DETAIL_URL_NAME = "post_detail"
LOGIN_URL_NAME = "login"

POST_DATA = {
    "title": "new title",
    "description": "description",
    "uploaded_file": "uploads/uploaded_file.jpeg",
    "thumbnail_image": "thumbnail_images/image.jpeg",
    "owner": 1,
    "file_type": 1,
    "is_private": False,
}


@pytest.mark.parametrize(
    "post_id, status_code",
    [
        (1, 200),
        (0, 404),
    ],
)
def test_detail_view_post_with_id_exists(client, post, post_id, status_code):
    """
    The detail view of post to check if post is accesible
    if post exists, otherwise a 404 error is thrown
    """

    url = reverse(POST_DETAIL_URL_NAME, args=(post_id,))
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "url_name, status_code",
    [
        (DASHBOARD_URL_NAME, 302),
        (POST_CREATE_URL_NAME, 302),
        (POST_UPDATE_URL_NAME, 302),
        (POST_DELETE_URL_NAME, 302),
    ],
)
def test_redirection_in_views(client, post, url_name, status_code):
    """
    Testing redirection in views where login is required
    """

    login_url = reverse(LOGIN_URL_NAME)

    if url_name in [POST_UPDATE_URL_NAME, POST_DELETE_URL_NAME]:
        url = reverse(url_name, args=(post.id,))
    else:
        url = reverse(url_name)

    response = client.get(url)
    assert response["location"] == f"{login_url}?next={url}"
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "url_name, status_code",
    [
        (POST_UPDATE_URL_NAME, 403),
        (POST_DELETE_URL_NAME, 403),
    ],
)
def test_post_update_delete_when_user_is_not_author(
    post, user, client, url_name, status_code
):
    """
    Testing post update and delete when user is not the real author
    """
    client.force_login(user)
    url = reverse(url_name, args=(post.id,))
    response = client.get(url)
    assert response.status_code == status_code


def test_delete_post_with_user_real_author(post, client):
    """
    Test to check if post is deleted when the original author is
    deleting it
    """

    client.force_login(post.owner)
    url = reverse(POST_DELETE_URL_NAME, args=(post.id,))
    response = client.delete(url)

    assert response["location"] == reverse(HOME_URL_NAME)
    assert response.status_code == 302
    assert Post.objects.count() == 0


def test_update_post_with_user_real_author(post, client):
    """
    Test to check if post is updated when the original author is
    updating it
    """

    client.force_login(post.owner)
    url = reverse(POST_UPDATE_URL_NAME, args=(post.id,))

    post_data = POST_DATA
    post_data["owner"] = post.owner

    response = client.post(
        url,
        data=POST_DATA,
    )

    post.refresh_from_db()

    assert response["location"] == reverse(DASHBOARD_URL_NAME)
    assert response.status_code, 302
    assert post.title == "new title"


@pytest.mark.parametrize(
    "url_name, status_code",
    [
        (DASHBOARD_URL_NAME, 200),
        (POST_UPDATE_URL_NAME, 200),
        (POST_DELETE_URL_NAME, 200),
    ],
)
def test_logged_in_can_access_dashboard_update_delete_view(
    client, post, url_name, status_code
):
    """
    Testing if user can access dashboard if he's logged in
    """

    client.force_login(post.owner)

    if url_name in [POST_UPDATE_URL_NAME, POST_DELETE_URL_NAME]:
        url = reverse(url_name, args=(post.id,))
    else:
        url = reverse(url_name)

    response = client.get(url)
    assert response.status_code == status_code


def test_logged_in_user_can_create_post(client, user):
    """
    Testing user can create post after logging in
    """

    client.force_login(user)
    post_create_url = reverse(POST_CREATE_URL_NAME)
    dashboard_url = reverse(DASHBOARD_URL_NAME)

    uploaded_file = SimpleUploadedFile(
        name="uploaded_file.jpg", content=open("media/default.jpg", "rb").read()
    )
    thumnail_image = SimpleUploadedFile(
        name="thumnail_image.jpg",
        content=open("media/default.jpg", "rb").read(),
        content_type="image/jpeg",
    )

    post_data = POST_DATA
    post_data["owner"] = user
    post_data["uploaded_file"] = uploaded_file
    post_data["thumnail_image"] = thumnail_image

    response = client.post(post_create_url, post_data)
    assert Post.objects.last().title == "new title"
    assert response["location"] == dashboard_url
    assert response.status_code == 302


def test_list_view_homepage(client, posts):
    """
    Testing if 10 posts are displayed on the homepage
    """

    post_id = 10

    home_url = reverse(HOME_URL_NAME)
    response = client.get(home_url)

    assert response.status_code == 200
    assert response.context["Posts"].count() == 10

    for post in response.context["Posts"]:
        assert post.title == f"post {post_id}"
        post_id -= 1


def test_private_post_not_visible_to_visitors(client, private_post):
    """
    Testing if private post should not be visible to visitors
    """
    home_url = reverse(HOME_URL_NAME)
    response = client.get(home_url)

    assert response.status_code == 200
    assert response.context["Posts"].count() == 0


def test_private_post_visible_to_original_author(client, post):
    """
    Testing if private post is visible to original author
    """
    client.force_login(post.owner)

    home_url = reverse(HOME_URL_NAME)
    response = client.get(home_url)

    assert response.status_code == 200
    assert response.context["Posts"].count() == 1
