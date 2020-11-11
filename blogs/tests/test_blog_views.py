from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from rest_framework import status
from rest_framework.test import APIClient

from blogs.models import Blog, Tag
from blogs.serializers import MyBlogSerializer


BLOGS_URL = reverse('blogs:blog-list')
MY_BLOGS_URL = reverse('blogs:blog-me')


def detail_url(blog_slug):
    """Return blog detail URL"""
    return reverse('blogs:blog-detail', args=[blog_slug])


def sample_blog(author, **params):
    """Create and return a sample blog"""
    defaults = {
        'title': 'Some funny title',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    defaults.update(params)

    return Blog.objects.create(author=author, **defaults)


def create_tag(content):
    """Create and return Tag"""
    return Tag.objects.create(content=content)


class PublicBlogAPITest(TestCase):
    """Test unauthenticated blog API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(BLOGS_URL)

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

    def test_retrieve_blogs(self):
        """Test retrieving a list of blogs"""
        payload1 = {
            'title': 'Normalize database',
            'content': 'Lorem ipsum dolor sit amet, consectetur'
        }
        blog1 = self.client.post(BLOGS_URL, payload1)

        payload2 = {
            'title': 'Django REST',
            'content': 'Lorem ipsum dolor sit amet, consectetur'
        }
        blog2 = self.client.post(BLOGS_URL, payload2)

        res = self.client.get(BLOGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], blog2.data)
        self.assertEqual(res.data[1], blog1.data)

    def test_create_minimum_blog(self):
        """Test creating blog"""
        title = 'Normalize database'
        payload = {
            'title': title,
            'content': 'Lorem ipsum dolor sit amet, consectetur'
        }

        res = self.client.post(BLOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(slugify(title), res.data['slug'])

        blog = Blog.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(blog, key))

    def test_blog_detail_view(self):
        """Test viewing a blog detail"""
        payload = {
            'title': 'Normalize database',
            'content': 'Lorem ipsum dolor sit amet, consectetur'
        }

        blog = self.client.post(BLOGS_URL, payload)

        url = detail_url(blog.data['slug'])

        res = self.client.get(url)

        self.assertEqual(res.data, blog.data)

    def test_update_blogs_only_authors(self):
        user2 = get_user_model().objects.create_user(
            username='testupdate',
            password='testpassword'
        )

        blog = sample_blog(author=user2)

        payload = {
            'content': 'Updating content'
        }

        url = detail_url(blog.slug)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_blog(self):
        """Test updating a blog with PATCH"""
        blog = sample_blog(author=self.user)

        payload = {
            'content': 'Updating content'
        }

        url = detail_url(blog.slug)

        self.client.patch(url, payload)

        blog.refresh_from_db()

        self.assertEqual(blog.content, payload['content'])
        self.assertNotEqual(blog.created_at, blog.updated_at)

    def test_full_update_blog(self):
        """Test updating a blog with PUT"""
        blog = sample_blog(author=self.user)

        payload = {
            'title': 'Some funny title',
            'content': 'Updating content'
        }

        url = detail_url(blog.slug)

        self.client.put(url, payload)

        blog.refresh_from_db()

        self.assertEqual(blog.content, payload['content'])

    def test_delete_blog(self):
        """Test deleting a blog with DELETE"""
        blog = sample_blog(author=self.user)

        url = detail_url(blog.slug)

        self.client.delete(url)

        blog_exists = Blog.objects.filter(
            id=blog.id
        ).exists()

        self.assertFalse(blog_exists)

    def test_likes_count_in_blog(self):
        """Test the like counting in blog"""
        new_blog = sample_blog(author=self.user)

        user2 = get_user_model().objects.create_user(
            username='testlikes2',
            password='testpassword'
        )
        user3 = get_user_model().objects.create_user(
            username='testlikes3',
            password='testpassword'
        )

        new_blog.likes.add(user2)
        new_blog.likes.add(user3)

        url = detail_url(new_blog.slug)

        res = self.client.get(url)

        self.assertEqual(res.data['likes_count'], 2)

    def test_user_has_liked_field_in_blog(self):
        """Test the user_has_liked in blog"""
        blog = sample_blog(author=self.user)
        blog.likes.add(self.user)

        url = detail_url(blog.slug)
        res = self.client.get(url)

        self.assertEqual(res.data['likes_count'], 1)
        self.assertEqual(res.data['user_has_liked'], True)

    def test_retrieve_blogs_limited_to_user(self):
        """Test retrieving only user blogs in blogs-me URL"""
        user2 = get_user_model().objects.create_user(
            username='testmyblogs',
            password='testpassword'
        )

        sample_blog(author=self.user)

        sample_blog(
            author=user2,
            title='Limited to user',
            content='blabalbalbalbalblaab'
        )

        res = self.client.get(MY_BLOGS_URL)

        blogs = Blog.objects.filter(author=self.user)
        serializer = MyBlogSerializer(blogs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_blog_with_tags_successfully(self):
        """Test create blog with existent tags successfully"""
        tag1 = create_tag('Tech')
        tag2 = create_tag('Apple')

        payload = {
            'title': 'Macbook Pro is really Pro?',
            'content': 'Lorem ipsum dolor sit amet, consectetur',
            'tags': [
                tag1.id,
                tag2.id
            ]
        }

        res = self.client.post(BLOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        blog = Blog.objects.get(id=res.data['id'])

        blogtag1 = blog.tags.filter(id=1).exists()
        blogtag2 = blog.tags.filter(id=2).exists()

        self.assertTrue(blogtag1)
        self.assertTrue(blogtag2)

    def test_createblog_with_invalid_tags(self):
        """Test create blog with invalid tags"""

        payload = {
            'title': 'Macbook Pro is really Pro?',
            'content': 'Lorem ipsum dolor sit amet, consectetur',
            'tags': {
                1
            }
        }

        res = self.client.post(BLOGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
