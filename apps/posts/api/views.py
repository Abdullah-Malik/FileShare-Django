"""
Views used in Restful APIs of posts app
"""

from django.db.models import Q
from django.http.response import JsonResponse

from ..models import Post
from .serializers import PostSerializer


def PostSearchAPI(request):
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


def PostCommentAPI(request):
    """
    Function saves the comment POST request
    """
    if request.method == "POST":
        print(request.data)
