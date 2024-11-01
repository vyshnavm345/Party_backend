from django.urls import path

from .views import (
    EventDetailView,
    EventListCreateView,
    NewsFeedDetailView,
    NewsFeedListCreateView,
)

urlpatterns = [
    path("", NewsFeedListCreateView.as_view(), name="newsfeed-list-create"),
    path("<int:pk>/", NewsFeedDetailView.as_view(), name="newsfeed-detail"),
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
]
