from django.urls import path, include

from rest_framework.routers import DefaultRouter

from blogs import views as BlogViews


router = DefaultRouter()
router.register(r'tags', BlogViews.CreateListTagAPIViewSet)
router.register(r'blogs', BlogViews.BlogViewSet)

app_name = 'blogs'

urlpatterns = [
    path(
        'blogs/me/',
        BlogViews.MyblogsAPIView.as_view(),
        name='blog-me'
    ),

    path(
        '',
        include(router.urls)
    ),

    path(
        'tags/blog/<slug:slug>/',
        BlogViews.ListBlogTagsAPIView.as_view(),
        name='blog-tags'
    ),

    path(
        'blogs/like/<int:id>/',
        BlogViews.BlogLikeAPIView.as_view(),
        name='blog-like'
    ),

    path(
        'blogs/<slug:slug>/new/comment/',
        BlogViews.CommentCreateAPIView.as_view(),
        name='comment-create'
    ),

    path(
        'blogs/<slug:slug>/comments/',
        BlogViews.CommentListAPIView.as_view(),
        name='comment-list'
    ),

    path(
        'comments/<int:pk>/',
        BlogViews.CommentRetrieveUpdateDestroyAPIView.as_view(),
        name='comment-detail'
    ),

    path(
        'comments/like/<int:id>/',
        BlogViews.CommentLikeAPIView.as_view(),
        name='comment-like'
    ),
]
