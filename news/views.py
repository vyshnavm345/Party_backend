from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import NewsFeed
from .serializers import NewsSerializer


class NewsFeedListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer


class NewsFeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = NewsFeed.objects.all()
    serializer_class = NewsSerializer
