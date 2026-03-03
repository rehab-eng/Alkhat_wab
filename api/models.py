import uuid

from django.db import models
from django_resized import ResizedImageField


class Truck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = ResizedImageField(
        size=[800, 600],
        quality=75,
        force_format='WEBP',
        upload_to='trucks/',
    )

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = ResizedImageField(
        size=[800, 600],
        quality=75,
        force_format='WEBP',
        upload_to='projects/',
    )

    def __str__(self) -> str:
        return self.title


class Stat(models.Model):
    STAT_CHOICES = [
        ('years', 'Years of Experience'),
        ('projects', 'Mega Projects'),
        ('fleet', 'Fleet Units'),
        ('safety', 'Safety Index'),
    ]

    key = models.CharField(max_length=32, unique=True, choices=STAT_CHOICES)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return f'{self.get_key_display()} ({self.value}{self.suffix})'


class Vehicle(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = ResizedImageField(
        size=[800, 600],
        quality=75,
        force_format='WEBP',
        upload_to='vehicles/',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-id']

    def __str__(self) -> str:
        return self.title


class Statistic(models.Model):
    key = models.CharField(max_length=32, unique=True)
    label_en = models.CharField(max_length=120)
    label_ar = models.CharField(max_length=120, blank=True)
    caption_en = models.CharField(max_length=200, blank=True)
    caption_ar = models.CharField(max_length=200, blank=True)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return f'{self.key}: {self.value}{self.suffix}'


class SiteSetting(models.Model):
    site_name_en = models.CharField(max_length=200, blank=True)
    site_name_ar = models.CharField(max_length=200, blank=True)
    hero_title_en = models.CharField(max_length=200, blank=True)
    hero_title_ar = models.CharField(max_length=200, blank=True)
    hero_desc_en = models.TextField(blank=True)
    hero_desc_ar = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    address_ar = models.CharField(max_length=255, blank=True)
    logo = ResizedImageField(
        size=[800, 600],
        quality=75,
        force_format='WEBP',
        upload_to='settings/',
        blank=True,
        null=True,
    )
    hero_image = ResizedImageField(
        size=[800, 600],
        quality=75,
        force_format='WEBP',
        upload_to='settings/',
        blank=True,
        null=True,
    )
    refresh_token = models.UUIDField(default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-id']

    def __str__(self) -> str:
        return self.site_name_en or 'Site Settings'
