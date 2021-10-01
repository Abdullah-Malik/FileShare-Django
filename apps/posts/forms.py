"""
Module contains information regarding the forms that Posts app is using
"""

from django import forms

from .models import Comment, Post


class CommentsForm(forms.ModelForm):
    """
    CommentsForm is used in the PostDetailView to allowing users
    to add comments under posts
    """

    class Meta:
        """
        Meta information of CommentsForm
        """

        model = Comment
        fields = [
            "comment_text",
        ]


class PostsForm(forms.ModelForm):
    """
    PostsForm is used in the PostCreateView and PostUpdateView to enable 
    users to create and update posts
    """

    class Meta:
        """
        Meta information of CommentsForm
        """

        model = Post
        fields = [
            "title",
            "description",
            "uploaded_file",
            "thumbnail_image",
            "file_type",
            "is_private",
        ]
        widgets = {"file_type": forms.RadioSelect()}
