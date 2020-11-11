from django.db import models
from django.contrib.auth.models import AbstractUser


class ViBlogUser(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True)
    biography = models.TextField(null=True)
