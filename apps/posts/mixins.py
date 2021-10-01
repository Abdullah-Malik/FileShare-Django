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
        Fetch the queryset from the parent's get_queryset

        Return:
            queryset: set of objects that meet the filteration criteria
        """
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        print(q, queryset)
        return queryset
