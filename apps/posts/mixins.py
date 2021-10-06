"""
Custom Mixins for Posts app
"""
from django.db.models import Q


class TitleDescriptionSearchMixin:
    """
    Custom Mixin for Searching Posts
    """

    def get_queryset(self):
        """
        queryset: set of objects that contain the query words either
        in title or description
        """
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset
