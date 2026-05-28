import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    genres = models.ManyToManyField(Genre, related_name="albums", blank=True)
    year = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="albums/", null=True, blank=True)

    class Meta:
        unique_together = ("title", "artist")

    def __str__(self):
        return f"{self.artist} - {self.title}"

    def get_absolute_url(self):
        return reverse("vinyl:album-detail", kwargs={"pk": self.pk})

    @property
    def cover_url(self):

        if self.cover and hasattr(self.cover, "url"):
            return self.cover.url

        path = os.path.join(settings.MEDIA_ROOT, "albums", f"{self.id}.jpg")

        if os.path.exists(path):
            return f"{settings.MEDIA_URL}albums/{self.id}.jpg"

        return static("img/default-album.jpg")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover:
            ext = os.path.splitext(self.cover.name)[1]

            new_name = f"{self.pk}{ext}"

            new_path = os.path.join(
                settings.MEDIA_ROOT,
                "albums",
                new_name
            )

            if self.cover.path != new_path:
                if os.path.exists(new_path):
                    os.remove(new_path)

                os.rename(self.cover.path, new_path)

                self.cover.name = f"albums/{new_name}"

                super().save(update_fields=["cover"])



class Collection(models.Model):
    STATUS_TYPE = (
        ("owned", "Owned"),
        ("wishlist", "Wishlist"),
        ("trade", "Trade"),
    )
    CONDITION_TYPE = (
        ("SS", "Sealed"),
        ("M", "Mint"),
        ("NM", "Near Mint"),
        ("EX", "Excellent"),
        ("VG", "Very Good"),
        ("G", "Good"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collection"
    )
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="in_collections"
    )
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default="owned")
    rating = models.IntegerField(null=True, blank=True)
    condition = models.CharField(
        max_length=2, choices=CONDITION_TYPE, default="NM", blank=True
    )

    class Meta:
        unique_together = ("user", "album")

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.album.title} "
            f"({self.get_status_display()})"
        )


class User(AbstractUser):
    country = models.CharField(max_length=63, null=True, blank=True)

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return self.username
