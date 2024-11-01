from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


# Create your models here.
class NewsFeed(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="news_feed_images/", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.date}"


class News(Page):
    description = models.TextField()
    image = models.ImageField(upload_to="news_feed_images/", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    def __str__(self) -> str:
        return str(self.date)


class Event(Page):
    heading = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="news_feed_images/", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]
