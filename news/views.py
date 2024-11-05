from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import EventsFeed, NewsFeed
from .pagination import StandardResultsSetPagination
from .serializers import EventSerializer, NewsSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all().order_by("-date")
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = EventsFeed.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventsFeed.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
