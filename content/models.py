import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Hashtag(models.Model):
    name = models.CharField(max_length=255)


class Post(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts"
    )
    hashtags = models.ManyToManyField(
        Hashtag, related_name="posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}: {self.content[:20]}"

    class Meta:
        ordering = ["-created_at"]


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.owner.full_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=movie_image_file_path, blank=True, null=True
    )
