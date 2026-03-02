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
