from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Event, NewsFeed
from .serializers import EventSerializer, NewsSerializer


class NewsFeedListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer


class NewsFeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
