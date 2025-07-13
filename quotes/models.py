from django.db import models, transaction
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.author:
            return f"{self.name} (author: {self.author})"
        return self.name


class Quote(models.Model):
    MIN_WEIGHT, MAX_WEIGHT = 0, 10
    MAX_QUOTES_PER_SOURCE = 3

    text = models.TextField(unique=True)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
    )
    weight = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(MIN_WEIGHT), MaxValueValidator(MAX_WEIGHT)],
    )
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = f"{self.text[:25]}..." if len(self.text) > 25 else self.text
        return f"{text} (weight: {self.weight}, likes: {self.likes}, dislikes: {self.dislikes})"

    def _check_quotes_limit(self):
        if not self.pk and self.source_id:
            quotes_count = Quote.objects.filter(source_id=self.source_id).count()
            if quotes_count >= self.MAX_QUOTES_PER_SOURCE:
                raise ValidationError(
                    f"A source cannot have more than {self.MAX_QUOTES_PER_SOURCE} quotes.",
                    code="quotes_limit_exceeded",
                    params={"max": self.MAX_QUOTES_PER_SOURCE},
                )

    def clean(self):
        self._check_quotes_limit()
        super().clean()

    def save(self, *args, **kwargs):
        if not self.pk and self.source_id:
            with transaction.atomic():
                source = Source.objects.select_for_update().get(pk=self.source_id)
                self._check_quotes_limit()
                return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def add_view(self):
        self.views = F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db()

    def add_like(self):
        self.likes = F('likes') + 1
        self.save(update_fields=['likes'])
        self.refresh_from_db()

    def add_dislike(self):
        self.dislikes = F('dislikes') + 1
        self.save(update_fields=['dislikes'])
        self.refresh_from_db()
