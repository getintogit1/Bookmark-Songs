
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import os
from django.utils import timezone


def image_upload_path(instance, filename):
    """
    MEDIA_ROOT/images/YYYY/MM/DD/filename.ext
    """
    today = timezone.now()
    return os.path.join(
        'images',
        str(today.year),
        f'{today.month:02}',
        f'{today.day:02}',
        filename
    )

class Song(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tracks_created',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200, null=True, blank=True)
    artist = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True,default='default-album-img.svg')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='songs_liked',
        blank=True,
    )
    total_likes = models.PositiveIntegerField(default=0)
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes'])
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('songs:detail', args=[self.id, self.slug])




