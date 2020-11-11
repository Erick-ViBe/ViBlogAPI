from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Tag to be used to clasify blogs"""
    content = models.CharField(max_length=25, unique=True)

    def save(self, *args, **kwargs):
        self.content = self.content.lower()
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.content


class Blog(models.Model):
    """Blog object"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=240)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="blogs")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="liked_blogs")
    tags = models.ManyToManyField('Tag',
                                  related_name="tag_blogs")

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Blogs comments"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="comments")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="liked_comments")
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             related_name="comments")

    def __str__(self):
        return self.content
