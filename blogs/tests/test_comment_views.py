from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from blogs.models import Blog, Comment


def create_comment_url(blog_slug):
    """Return create comment URL"""
    return reverse('blogs:comment-create', args=[blog_slug])


def retrieve_comments_url(blog_slug):
    """Return retrieve comment URL"""
    return reverse('blogs:comment-list', args=[blog_slug])


def detail_comment_url(comment_id):
    """Return detail comment URL"""
    return reverse('blogs:comment-detail', args=[comment_id])


def sample_blog(author, **params):
    """Create and return a sample blog"""
    defaults = {
        'title': 'Some funny title',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    defaults.update(params)

    return Blog.objects.create(author=author, **defaults)


class PublicBlogAPITest(TestCase):
    """Test unauthenticated blog API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_create_comment(self):
        """Test that authentication is required to create new comment"""
        user2 = get_user_model().objects.create_user(
            username='testauth',
            password='testpassword'
        )

        blog = sample_blog(author=user2)

        payload = {
            'content': 'viblog funny comment'
        }

        url = create_comment_url(blog.slug)

        res = self.client.post(url, payload)

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

    def test_create_comment(self):
        """Test creating a comment"""
        blog = sample_blog(author=self.user)

        payload = {
            'content': 'viblog funny comment'
        }

        url = create_comment_url(blog.slug)

        res = self.client.post(url, payload)

        self.assertEqual(payload['content'], res.data['content'])

        comment_exist = Comment.objects.filter(id=res.data['id']).exists()

        self.assertTrue(comment_exist)

    def test_retrieve_blog_comments(self):
        """Test retrieving a blog comments"""
        blog = sample_blog(author=self.user)

        comment1 = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        comment2 = Comment.objects.create(
            author=self.user,
            content='Blabla content some',
            blog=blog
        )

        url = retrieve_comments_url(blog.slug)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['content'], comment2.content)
        self.assertEqual(res.data[1]['content'], comment1.content)

    def test_blog_detail_view(self):
        """Test viewing a blog detail"""
        blog = sample_blog(author=self.user)

        payload = {
            'content': 'viblog funny comment'
        }

        url = create_comment_url(blog.slug)

        comment = self.client.post(url, payload)

        url = detail_comment_url(comment.data['id'])

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(comment.data, res.data)

    def test_update_comment_only_authors(self):
        """Test only author may update the comment"""
        blog = sample_blog(author=self.user)

        user2 = get_user_model().objects.create_user(
            username='testupdate',
            password='testpassword'
        )

        comment = Comment.objects.create(
            author=user2,
            content='Some content blabla',
            blog=blog
        )

        payload = {
            'content': 'Updating content'
        }

        url = detail_comment_url(comment.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_comment(self):
        """Test updating a comment with PATCH"""
        blog = sample_blog(author=self.user)

        comment = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        payload = {
            'content': 'Updating content'
        }

        url = detail_comment_url(comment.id)

        self.client.patch(url, payload)

        comment.refresh_from_db()

        self.assertEqual(comment.content, payload['content'])
        self.assertNotEqual(comment.created_at, comment.updated_at)

    def test_full_update_blog(self):
        """Test updating a comment with PUT"""
        blog = sample_blog(author=self.user)

        comment = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        payload = {
            'content': 'Updating content'
        }

        url = detail_comment_url(comment.id)

        self.client.put(url, payload)

        comment.refresh_from_db()

        self.assertEqual(comment.content, payload['content'])
        self.assertNotEqual(comment.created_at, comment.updated_at)

    def test_delete_blog(self):
        """Test deleting a blog with DELETE"""
        blog = sample_blog(author=self.user)

        comment = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        url = detail_comment_url(comment.id)

        self.client.delete(url)

        comment_exists = Comment.objects.filter(
            id=comment.id
        ).exists()

        self.assertFalse(comment_exists)

    def test_likes_count_in_comment(self):
        """Test the like counting in comment"""
        blog = sample_blog(author=self.user)

        comment = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        user2 = get_user_model().objects.create_user(
            username='testlikes2',
            password='testpassword'
        )
        user3 = get_user_model().objects.create_user(
            username='testlikes3',
            password='testpassword'
        )

        comment.likes.add(user2)
        comment.likes.add(user3)

        url = detail_comment_url(comment.id)

        res = self.client.get(url)

        self.assertEqual(res.data['likes_count'], 2)

    def test_user_has_liked_field_in_blog(self):
        """Test the user_has_liked in blog"""
        blog = sample_blog(author=self.user)

        comment = Comment.objects.create(
            author=self.user,
            content='Some content blabla',
            blog=blog
        )

        comment.likes.add(self.user)

        url = detail_comment_url(comment.id)

        res = self.client.get(url)

        self.assertEqual(res.data['likes_count'], 1)
        self.assertEqual(res.data['user_has_liked'], True)
