"""
Description of Serializers in the users app
"""
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Post Serializer is used in PostSearchAPIview to serialize the
    User model data
    """

    profile_url = serializers.HyperlinkedIdentityField(
        view_name="profile", lookup_field="username"
    )

    class Meta:
        """
        Meta information
        """

        model = User
        fields = ["username", "first_name", "last_name", "image", "profile_url"]
