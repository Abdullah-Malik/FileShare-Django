"""
unit tests for post app views
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.posts.models import Post
from apps.users.models import User

factory = RequestFactory()


class TestPostView(TestCase):
    """
    Class contains tests for views in post app
    """

    def setUp(self):
        """
        Setup function creates an object and stores it in database
        for testing
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

    def test_detail_view_post_with_id_exists(self):
        """
        The detail view of a question with an id that is in the database
        returns a 200 status.
        """

        url = reverse("post_detail", args=(self.post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_post_with_id__does_not_exist(self):
        """
        The detail view of a question with an id that is not in the database
        returns a 404 not found.
        """
        url_404_page = reverse("post_detail", args=(0,))
        response = self.client.get(url_404_page)
        self.assertEqual(response.status_code, 404)

    def test_update_view_redirection(self):
        """
        Test to check redirection if user is not logged in
        only logged in user can update post
        """
        login_url = reverse("login")
        url = reverse("post_update", args=(self.post.id,))
        response = self.client.get(url)
        self.assertRedirects(
            response, "{login_url}?next={url}".format(login_url=login_url, url=url)
        )

    def test_delete_view_redirection(self):
        """
        Test to check redirection if user is not logged in
        only logged in user can delete post
        """
        login_url = reverse("login")
        url = reverse("post_delete", args=(self.post.id,))
        response = self.client.get(url)
        self.assertRedirects(
            response, "{login_url}?next={url}".format(login_url=login_url, url=url)
        )

    def test_create_view_redirection(self):
        """
        Test to check redirection if user is not logged in
        only logged in user can create post
        """
        login_url = reverse("login")
        url = reverse("post_create")
        response = self.client.get(url)
        self.assertRedirects(
            response, "{login_url}?next={url}".format(login_url=login_url, url=url)
        )

    def test_dashboard_view_redirection(self):
        """
        Test to check redirection if user is not logged in
        only logged in user can access a dashboard
        """
        login_url = reverse("login")
        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertRedirects(
            response, "{login_url}?next={url}".format(login_url=login_url, url=url)
        )

    def test_update_post_with_user_not_the_real_author(self):
        """
        Test to check if user trying to update a post is the author
        of the post otherwise a 403 code is returned
        """
        my_username = "jane"
        my_password = "321"
        my_email = "jane@doe.com"
        User.objects.create_user(
            username=my_username, email=my_email, password=my_password
        )
        self.client.login(username=my_username, password=my_password)

        url = reverse("post_update", args=(self.post.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_update_post_with_user_real_author(self):
        """
        Test to check if post is updated when the original author is
        updating it
        """

        my_post = Post.objects.create(
            title="title2",
            description="description",
            uploaded_file="uploads/uploaded_file.jpeg",
            thumbnail_image="thumbnail_images/image.jpeg",
            owner=self.user,
            file_type=1,
            is_private=False,
        )

        self.client.login(username=self.username, password=self.password)

        url = reverse("post_update", args=(my_post.id,))
        response = self.client.post(
            url,
            data={
                "title": "new title",
                "description": "description",
                "uploaded_file": "uploads/uploaded_file.jpeg",
                "thumbnail_image": "thumbnail_images/image.jpeg",
                "owner": self.user,
                "file_type": 1,
                "is_private": False,
            },
        )

        self.assertEqual(response.status_code, 302)
        my_post.refresh_from_db()
        self.assertEqual(my_post.title, "new title")

    def test_delete_post_with_user_not_the_real_author(self):
        """
        Test to check if user trying to delete a post is the author
        of the post otherwise a 403 code is returned
        """
        my_username = "jane"
        my_password = "321"
        my_email = "jane@doe.com"
        User.objects.create_user(
            username=my_username, email=my_email, password=my_password
        )
        self.client.login(username=my_username, password=my_password)

        url = reverse("post_delete", args=(self.post.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_post_with_user_real_author(self):
        """
        Test to check if post is updated when the original author is
        updating it
        """

        my_post = Post.objects.create(
            title="title2",
            description="description",
            uploaded_file="uploads/uploaded_file.jpeg",
            thumbnail_image="thumbnail_images/image.jpeg",
            owner=self.user,
            file_type=1,
            is_private=False,
        )

        self.assertEqual(Post.objects.count(), 2)
        self.client.login(username=self.username, password=self.password)

        url = reverse("post_delete", args=(my_post.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

    def test_dashboard_view_access_with_user_logged_in(self):
        """
        Testing if user is able to access dashboard when he is logged in
        """
        self.client.login(username=self.username, password=self.password)
        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_create_post(self):
        """
        Testing if a logged in user can create post
        """

        self.client.login(username=self.username, password=self.password)
        post_create_url = reverse("post_create")
        dashboard_url = reverse("dashboard")

        uploaded_file = SimpleUploadedFile(
            name="uploaded_file.jpg", content=open("media/default.jpg", "rb").read()
        )
        thumnail_image = SimpleUploadedFile(
            name="thumnail_image.jpg",
            content=open("media/default.jpg", "rb").read(),
            content_type="image/jpeg",
        )

        post_data = {
            "title": "new title",
            "description": "new description",
            "is_private": False,
            "file_type": 1,
            "uploaded_file": uploaded_file,
            "thumnail_image": thumnail_image,
        }

        response = self.client.post(post_create_url, post_data)
        self.assertEqual(Post.objects.last().title, "new title")
        self.assertRedirects(response, dashboard_url)

    def test_list_view_homepage_user_not_logged_in_checking_posts_order(self):
        """
        Test the post order which should be in the descending order of
        date posted. In this test case, user is not logged in.
        """

        home_url = reverse("home")

        post = Post()
        post.title = "title2"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = self.user
        post.file_type = "1"
        post.is_private = False
        post.save()

        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Posts"].count(), 2)
        self.assertEqual(response.context["Posts"].first().title, "title2")
        self.assertEqual(response.context["Posts"].last().title, "title1")

    def test_list_view_homepage_user_not_logged_in_checking_private_posts(self):
        """
        Test to check if private posts appear on homepage when the user is not
        logged in.
        """

        home_url = reverse("home")

        post = Post()
        post.title = "title2"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = self.user
        post.file_type = "1"
        post.is_private = True
        post.save()

        post = Post()
        post.title = "title3"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = User.objects.create_user(
            username="abdullah", password="arbisoft", email="abdullah@gmail.com"
        )
        post.file_type = "1"
        post.is_private = False
        post.save()

        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Posts"].count(), 2)
        self.assertEqual(response.context["Posts"].first().title, "title3")
        self.assertEqual(response.context["Posts"].last().title, "title1")

    def test_list_view_homepage_user_logged_in_checking_post_order(self):
        """
        Test the post order which should be in the descending order of
        date posted. In this test case, user is also logged in.
        """
        home_url = reverse("home")
        self.client.login(username=self.username, password=self.password)

        post = Post()
        post.title = "title2"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = self.user
        post.file_type = "1"
        post.is_private = True
        post.save()

        post = Post()
        post.title = "title3"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = User.objects.create_user(
            username="abdullah", password="arbisoft", email="abdullah@gmail.com"
        )
        post.file_type = "1"
        post.is_private = False
        post.save()

        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Posts"].count(), 3)
        self.assertEqual(response.context["Posts"].first().title, "title3")
        self.assertEqual(response.context["Posts"].last().title, "title1")

    def test_list_view_homepage_user_logged_in_checking_private_posts(self):
        """
        Test to check if private posts appear on homepage when the user is
        logged in.
        """
        home_url = reverse("home")
        self.client.login(username=self.username, password=self.password)

        post = Post()
        post.title = "title2"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = self.user
        post.file_type = "1"
        post.is_private = True
        post.save()

        post = Post()
        post.title = "title3"
        post.description = "description"
        post.uploaded_file = "uploads/uploaded_file.jpeg"
        post.thumbnail_image = "thumbnail_images/image.jpeg"
        post.owner = User.objects.create_user(
            username="abdullah", password="arbisoft", email="abdullah@gmail.com"
        )
        post.file_type = "1"
        post.is_private = True
        post.save()

        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Posts"].count(), 2)
        self.assertEqual(response.context["Posts"].first().title, "title2")
        self.assertEqual(response.context["Posts"].last().title, "title1")
