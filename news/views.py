from rest_framework import generics

from .models import NewsFeed
from .serializers import NewsSerializer


class NewsFeedListCreateView(generics.ListCreateAPIView):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer


class NewsFeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer
