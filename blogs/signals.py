from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_random_string
from blogs.models import Blog


@receiver(pre_save, sender=Blog)
def add_slug_to_blog(sender, instance, *args, **kwargs):
    """
    Signal added a slug base into the blog title,
    before create the Blog object
    """
    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string
