from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.author:
            return f"{self.name} (author: {self.author})"
        return self.name


class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
    )
    weight = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = f"{self.text[:25]}..." if len(self.text) > 25 else self.text
        return f"{text} (weight: {self.weight}, likes: {self.likes}, dislikes: {self.dislikes})"
