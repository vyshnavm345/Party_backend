from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import EventsFeed, NewsFeed

from .models import Banner
from .serializers import BannerSerializer, EventsFeedSerializer, NewsFeedSerializer


class HomePageView(APIView):
    def get(self, request):
        # Get current time and time 30 days ago
        current_time = timezone.now()
        past_30_days = current_time - timedelta(days=30)

        # Fetch banners
        banners = Banner.objects.all()

        # Fetch news and events created in the past 30 days
        recent_news = NewsFeed.objects.filter(date__gte=past_30_days).order_by("-date")[
            :10
        ]
        recent_events = EventsFeed.objects.filter(date__gte=past_30_days).order_by(
            "-date"
        )[:10]

        # If less than 10 news, fetch more from before 30 days
        if recent_news.count() < 10:
            additional_news = NewsFeed.objects.filter(date__lt=past_30_days).order_by(
                "-date"
            )[: 10 - recent_news.count()]
            recent_news = list(recent_news) + list(additional_news)

        # If less than 10 events, fetch more from before 30 days
        if recent_events.count() < 10:
            additional_events = EventsFeed.objects.filter(
                date__lt=past_30_days
            ).order_by("-date")[: 10 - recent_events.count()]
            recent_events = list(recent_events) + list(additional_events)

        # Serialize the data
        banner_data = BannerSerializer(banners, many=True).data
        news_data = NewsFeedSerializer(recent_news, many=True).data
        events_data = EventsFeedSerializer(recent_events, many=True).data

        # Create response data
        response_data = {
            "banners": banner_data,
            "news": news_data,
            "events": events_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
