from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from blogs.models import Tag, Blog

from blogs.serializers import TagSerializer


TAGS_URL = reverse('blogs:tag-list')


def blog_tags(blog_slug):
    """Return blog tags URL"""
    return reverse('blogs:blog-tags', args=[blog_slug])


class PublicTagsAPITests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testusername',
            'testpassword'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags_succesfully(self):
        """Test retrieving tags"""
        Tag.objects.create(content='tag1')
        Tag.objects.create(content='tag2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('content')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_tag_succesfully(self):
        """Test creating a new tag"""
        payload = {
            'content': 'test tag'
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Tag.objects.filter(
            content=payload['content']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {
            'content': ''
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_already_exists(self):
        """Test creating a tag that already exists fails"""
        Tag.objects.create(
            content='some tag'
        )

        payload = {
            'content': 'some tag'
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_only_in_lowercase(self):
        """Test creating a tag an save in lowercase"""
        payload = {
            'content': 'Test Tag'
        }

        self.client.post(TAGS_URL, payload)

        tag = Tag.objects.get(id=1)

        self.assertEqual(tag.content, payload['content'].lower())

    def test_list_tags_of_specific_blog(self):
        """Test retrieving blog tags"""
        tag1 = Tag.objects.create(content='tag1')
        tag2 = Tag.objects.create(content='tag2')

        blog = Blog.objects.create(
            author=self.user,
            title='test test test',
            content='alsjasfiusfiuasndfinsdfndf'
        )

        url = blog_tags(blog.slug)

        blog.tags.add(tag1)
        blog.tags.add(tag2)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data[0]['id'], tag1.id)
        self.assertEqual(res.data[0]['content'], tag1.content)
        self.assertEqual(res.data[1]['id'], tag2.id)
        self.assertEqual(res.data[1]['content'], tag2.content)
