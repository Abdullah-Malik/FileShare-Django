"""
Description of Models in the Posts app
"""

from django.db import models
from django.utils import timezone

from apps.users.models import User


class Post(models.Model):
    """
    Post model store information about posts.
    """

    FILE_TYPE_CHOICES = [
        (1, "Ebook"),
        (2, "Video"),
        (3, "Music"),
        (4, "Image"),
        (0, "Other"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_file = models.FileField(upload_to="uploads/")
    thumbnail_image = models.ImageField(
        default="default.jpg", upload_to="thumbnail_images"
    )
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, related_name="users_post", on_delete=models.CASCADE)
    file_type = models.IntegerField(choices=FILE_TYPE_CHOICES, default=0)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        """
        funtion returns the title of particular instance of Post object

        Return:
            it returns the title of particular instance of Post object
        """
        return f"{self.title}"


class Comment(models.Model):
    """
    Comment model stores information regarding comments under the posts
    """

    comment_text = models.TextField()
    author = models.ForeignKey(
        User, related_name="comment_author", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="comment_post", on_delete=models.CASCADE
    )
    comment_date_time = models.DateTimeField(editable=False, default=timezone.now)
