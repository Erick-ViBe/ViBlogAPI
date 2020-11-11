from rest_framework import viewsets, mixins, generics, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)

from blogs.serializers import (
    TagSerializer,
    BlogSerializer,
    MyBlogSerializer,
    CommentSerializer
)
from blogs.models import Tag, Blog, Comment
from blogs.permissions import IsAuthorOrReadOnly


class CreateListTagAPIViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """List and Create a new Tag"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('content')


class ListBlogTagsAPIView(generics.ListAPIView):
    """Retrieve blog tags"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('content')

    def get_queryset(self):
        """Retrieve blogs for the authenticated user"""
        kwarg_slug = self.kwargs.get("slug")
        return self.queryset.filter(tag_blogs__slug=kwarg_slug)


class BlogViewSet(viewsets.ModelViewSet):
    """Retrieve, update and delete Blogs"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all().order_by('-created_at')
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MyblogsAPIView(generics.ListAPIView):
    """Retrieve user blogs"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MyBlogSerializer
    queryset = Blog.objects.all().order_by('created_at')

    def get_queryset(self):
        """Retrieve blogs for the authenticated user"""
        return self.queryset.filter(author=self.request.user)


class BlogLikeAPIView(APIView):
    """Blog likes management"""
    serializer_class = BlogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        """Likes a blog"""
        blog = get_object_or_404(Blog, id=id)
        user = request.user

        blog.likes.add(user)
        blog.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(blog, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """Unlikes a blog"""
        blog = get_object_or_404(Blog, id=id)
        user = request.user

        blog.likes.remove(user)
        blog.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(blog, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(generics.CreateAPIView):
    """Create a new comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=kwarg_slug)

        if blog.comments.filter(author=request_user).exists():
            raise ValidationError("You have already commented this Blog!")

        serializer.save(author=request_user, blog=blog)


class CommentListAPIView(generics.ListAPIView):
    """Retrieve a blog comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve blog comments"""
        kwarg_slug = self.kwargs.get('slug')

        return self.queryset.filter(
            blog__slug=kwarg_slug
        ).order_by('-created_at')


class CommentRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """Comments detail view"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)


class CommentLikeAPIView(APIView):
    """Comment likes management"""
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        """Likes a comment"""
        comment = get_object_or_404(Comment, id=id)
        user = request.user

        comment.likes.add(user)
        comment.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """Unlikes a comment"""
        comment = get_object_or_404(Comment, id=id)
        user = request.user

        comment.likes.remove(user)
        comment.save()

        serializer_context = {'request': request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
