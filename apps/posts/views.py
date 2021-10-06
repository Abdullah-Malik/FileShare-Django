"""
Views in the the Posts apps
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentsForm, PostsForm
from .mixins import TitleDescriptionSearchMixin
from .models import Comment, Post


class PostDashboardView(LoginRequiredMixin, ListView):
    """
    A view where user can view the posts that he is author/owner of
    """

    template_name = "dashboard.html"
    context_object_name = "Posts"
    ordering = ["-date_posted"]

    def get_queryset(self):
        """
        get_queryset is used by ListViews to determine the list
        of objects that are to be displayed.
        """
        return Post.objects.filter(owner=self.request.user)


class PostListView(ListView):
    """
    A view where site visitor can view all the public posts created
    by any user
    """

    template_name = "home.html"
    context_object_name = "Posts"

    def get_queryset(self):
        """
        Return a list of post objects that are either public or which
        the logged in user is the author of
        """
        if not self.request.user.is_authenticated:
            return Post.objects.filter(is_private=False).order_by("-date_posted")

        return Post.objects.filter(
            Q(is_private=False) | Q(owner=self.request.user)
        ).order_by("-date_posted")


class PostDisplayView(DetailView):
    """
    A view that displays that information regarding one post object
    """

    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, *args, **kwargs):
        """
        Returns the context data to be displayed on the detail page
        """
        context = super().get_context_data(*args, **kwargs)
        context["comments"] = Comment.objects.filter(post=self.get_object())
        context["form"] = CommentsForm()
        return context


class PostDetailView(View):
    """
    Class extends the base View class and
    """

    def get(self, request, *args, **kwargs):
        """
        Function is called when a GET request is made

        return
            Returns a PostDisplayView
        """
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    PostUploadView extends the Create view and returns a view
    on which user can create a new post
    """

    model = Post
    template_name = "posts/post_create.html"
    form_class = PostsForm
    success_url = reverse_lazy("dashboard")
    success_message = "%(title)s Post was created successfully"

    def form_valid(self, form):
        """
        Method is called when valid form data is posted.
        It has been overridden to add owner (which is the logged in user)
        attributes to the request object before it is saved
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    """
    PostUpdateView is a view that displays a form for editing an
    existing post object, and saving changes made by the user
    """

    model = Post
    template_name = "posts/post_update.html"
    form_class = PostsForm
    success_url = reverse_lazy("dashboard")
    success_message = "%(title)s Post was updated successfully"

    def test_func(self):
        """
        test_func in the UserPassesTestMixin is overridden to check if the
        user updating the post was the original author of the post

        Parameters:
            self
        """
        post = self.get_object()
        if post.owner == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    PostDeleteView is a view that displays a confirmation page for
    deleting a post
    """

    model = Post
    success_url = reverse_lazy("home")
    template_name = "posts/post_delete.html"

    def test_func(self):
        """
        test_func in the UserPassesTestMixin is overridden to check if the
        user deleting the post was the original author of the post

        Parameters:
            self
        """
        post = self.get_object()
        if post.owner == self.request.user:
            return True
        return False


class PostSearchView(TitleDescriptionSearchMixin, ListView):
    """
    PostSearchView extends the ListView and uses the
    custom TitleSearchMixin for searching objects using the
    title provided in the query
    """

    model = Post
    template_name = "home.html"
    context_object_name = "Posts"
