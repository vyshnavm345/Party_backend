from django.urls import path

from .views import NewsFeedDetailView, NewsFeedListCreateView

urlpatterns = [
    path("", NewsFeedListCreateView.as_view(), name="newsfeed-list-create"),
    path("<int:pk>/", NewsFeedDetailView.as_view(), name="newsfeed-detail"),
]
