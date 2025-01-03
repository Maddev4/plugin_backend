import uuid
from django.db import models

class Deck(models.Model):
    deck_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    relevant_product = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.deck_id:
            self.deck_id = uuid.uuid4()
        super().save(*args, **kwargs)

class Slide(models.Model):
    slide_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deck = models.ForeignKey(Deck, related_name='slides', on_delete=models.CASCADE, null=True)
    slide_num = models.CharField(max_length=10)
    file_name = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    template_id = models.CharField(max_length=50, blank=True)
    shaped_id = models.CharField(max_length=50, blank=True)
    content = models.JSONField(default=dict)

    class Meta:
        ordering = ['slide_num']

    def __str__(self):
        return f"{self.file_name} - Slide {self.slide_num}"

    def save(self, *args, **kwargs):
        if not self.slide_id:
            self.slide_id = uuid.uuid4()
        super().save(*args, **kwargs) 