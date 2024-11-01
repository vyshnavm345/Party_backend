from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Event, News
from .pagination import StandardResultsSetPagination
from .serializers import EventSerializer, NewsSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all().order_by("-date")
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
