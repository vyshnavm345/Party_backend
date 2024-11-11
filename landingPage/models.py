from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Banner(models.Model):
    image = models.ImageField(upload_to="banner_images/")
    title = models.CharField(max_length=150, blank=True, null=True)
    link_url = models.URLField(blank=True, null=True, help_text="Optional link URL")

    panels = [
        FieldPanel("image"),
        FieldPanel("title"),
        FieldPanel("link_url"),
    ]

    def __str__(self):
        return f"Banner: {self.title or 'No Title'}"
