# serializers.py
from rest_framework import serializers

from news.models import EventsFeed, NewsFeed

from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["image", "title"]


class NewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = ["title", "description", "image", "date"]


class EventsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsFeed
        fields = ["title", "description", "image", "date"]
