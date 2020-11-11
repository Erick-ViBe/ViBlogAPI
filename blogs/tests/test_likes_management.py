from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from blogs.models import Blog, Comment


def blog_likes_url(blog_id):
    """Return liked blog url"""
    return reverse('blogs:blog-like', args=[blog_id])


def comment_likes_url(comment_id):
    """Return liked comment url"""
    return reverse('blogs:comment-like', args=[comment_id])


def sample_blog(author, **params):
    """Create and return a sample blog"""
    defaults = {
        'title': 'Some funny title',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    defaults.update(params)

    return Blog.objects.create(author=author, **defaults)


def sample_comment(author, blog, content='Funny content'):
    """Create and return a comment"""

    return Comment.objects.create(author=author, content=content, blog=blog)


class PublicBlogAPITest(TestCase):
    """Test unauthenticated blog API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_blog_like(self):
        """Test that authentication is required"""
        usertest = get_user_model().objects.create_user(
            username='publictest',
            password='testpassword'
        )

        blog = sample_blog(author=usertest)

        url = blog_likes_url(blog.id)

        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_comment_like(self):
        """Test that authentication is required"""
        usertest = get_user_model().objects.create_user(
            username='publictest',
            password='testpassword'
        )

        blog = sample_blog(author=usertest)

        comment = sample_comment(author=usertest, blog=blog)

        url = comment_likes_url(comment.id)

        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBlogAPITest(TestCase):
    """Test authenticated blog API access"""

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username='testusername',
            password='testpassword'
        )

        self.client.force_authenticate(self.user)

        self.blog = sample_blog(author=self.user)

    def test_get_blog_likes_url_not_allowed(self):
        """Test that POST is not allowed on the BLOG LIKES URL"""
        url = blog_likes_url(self.blog.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_like_a_blog_correctly(self):
        """Test post method likes_url to like a blog"""
        url = blog_likes_url(self.blog.id)

        self.client.post(url)

        self.blog.refresh_from_db()

        user_like = self.blog.likes.filter(id=self.user.id).exists()

        self.assertTrue(user_like)

        likes = self.blog.likes.count()

        self.assertEqual(likes, 1)

    def test_unlike_a_blog_correctly(self):
        """Test delete method likes_url to unlike a blog"""
        self.blog.likes.add(self.user)

        url = blog_likes_url(self.blog.id)

        self.client.delete(url)

        self.blog.refresh_from_db()

        user_like = self.blog.likes.filter(id=self.user.id).exists()

        self.assertFalse(user_like)

        likes = self.blog.likes.count()

        self.assertEqual(likes, 0)

    def test_get_comment_likes_url_not_allowed(self):
        """Test that GET is not allowed on the COMMENT LIKES URL"""
        blog = sample_blog(author=self.user)

        comment = sample_comment(author=self.user, blog=blog)

        url = comment_likes_url(comment.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_like_a_comment_correctly(self):
        """Test post method comment_likes_url to like a comment"""
        blog = sample_blog(author=self.user)

        comment = sample_comment(author=self.user, blog=blog)

        url = comment_likes_url(comment.id)

        self.client.post(url)

        comment.refresh_from_db()

        user_like = comment.likes.filter(id=self.user.id).exists()

        self.assertTrue(user_like)

        likes = comment.likes.count()

        self.assertEqual(likes, 1)

    def test_unlike_a_comment_correctly(self):
        """Test delete method comment_likes_url to unlike a comment"""
        blog = sample_blog(author=self.user)

        comment = sample_comment(author=self.user, blog=blog)

        comment.likes.add(self.user)

        url = comment_likes_url(comment.id)

        self.client.delete(url)

        comment.refresh_from_db()

        user_like = comment.likes.filter(id=self.user.id).exists()

        self.assertFalse(user_like)

        likes = comment.likes.count()

        self.assertEqual(likes, 0)
