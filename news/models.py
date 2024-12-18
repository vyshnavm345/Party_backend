from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class NewsFeed(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="news_feed_images/", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title


@register_snippet
class EventsFeed(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="news_feed_images/", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title
