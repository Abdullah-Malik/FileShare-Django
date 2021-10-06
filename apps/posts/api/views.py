"""
Views used in Restful APIs of posts app
"""

from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser

from ..models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


def post_search_api(request):
    """
    Function finds posts matching the query sent by the user

    Parameters:
        request: contains information regarding request

    Returns:
        Data related to the Posts matching the query in the json format
    """
    if request.method == "GET":
        q = request.GET.get("q")
        posts = Post.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"message": "No post matching the query found"})


class PostCommentList(generics.ListCreateAPIView):
    """
    Function saves the comment POST request
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


def post_comment_api(request):
    """
    Function saves the comment POST request
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
