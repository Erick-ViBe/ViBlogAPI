from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from blogs.models import Tag, Blog, Comment


def sample_user(username='testusername', password='testpassword'):
    """Created a sample user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            content='Tech'
        )

        self.assertEqual(str(tag), tag.content)

    def test_blog_str(self):
        """Test the blog string representation"""
        blog = Blog.objects.create(
            title='Some funny title',
            content='Some content blablablablablablablabla',
            author=sample_user()
        )

        self.assertEqual(str(blog), blog.title)

    def test_blog_slug(self):
        """Test when creating a blog, the slug is created correctly"""
        title = 'Some funny title'
        content = 'Some content blablablablablablablabla'

        blog = Blog.objects.create(
            title=title,
            content=content,
            author=sample_user()
        )

        self.assertIn(slugify(title), blog.slug)

    def test_comment_str(self):
        """Test the comment string representation"""
        title = 'Some funny title'
        content = 'Some content blablablablablablablabla'

        user = sample_user()

        blog = Blog.objects.create(
            title=title,
            content=content,
            author=user
        )

        comment = Comment.objects.create(
            author=user,
            content='Some funny content',
            blog=blog
        )

        self.assertEqual(str(comment), comment.content)
