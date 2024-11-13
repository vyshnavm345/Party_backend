from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from landingPage.models import Banner
from news.models import EventsFeed, NewsFeed


# Fixtures for reusable test data
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_banners():
    banners = [
        Banner.objects.create(title=f"Banner {i}", image=f"banner_{i}.jpg")
        for i in range(3)
    ]
    return banners


@pytest.fixture
def create_recent_news():
    current_time = timezone.now()
    recent_news = [
        NewsFeed.objects.create(
            title=f"Recent News {i}",
            description=f"Description {i}",
            image=f"news_{i}.jpg",
            date=current_time - timedelta(days=i),
        )
        for i in range(5)  # Creating 5 recent news items
    ]
    return recent_news


@pytest.fixture
def create_additional_news():
    past_time = timezone.now() - timedelta(days=31)
    additional_news = [
        NewsFeed.objects.create(
            title=f"Old News {i}",
            description=f"Old Description {i}",
            image=f"old_news_{i}.jpg",
            date=past_time - timedelta(days=i),
        )
        for i in range(5)  # Creating 5 old news items
    ]
    return additional_news


@pytest.fixture
def create_recent_events():
    current_time = timezone.now()
    recent_events = [
        EventsFeed.objects.create(
            title=f"Recent Event {i}",
            description=f"Event Description {i}",
            image=f"event_{i}.jpg",
            date=current_time - timedelta(days=i),
        )
        for i in range(5)  # Creating 5 recent events
    ]
    return recent_events


@pytest.fixture
def create_additional_events():
    past_time = timezone.now() - timedelta(days=31)
    additional_events = [
        EventsFeed.objects.create(
            title=f"Old Event {i}",
            description=f"Old Event Description {i}",
            image=f"old_event_{i}.jpg",
            date=past_time - timedelta(days=i),
        )
        for i in range(5)  # Creating 5 old events
    ]
    return additional_events


### **Test Cases**
@pytest.mark.django_db
def test_home_page_view_with_no_data(client):
    """Test the home page view with no data."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["banners"] == []
    assert response.data["news"] == []
    assert response.data["events"] == []


@pytest.mark.django_db
def test_home_page_view_with_banners(client, create_banners):
    """Test the home page view with banners."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["banners"]) == 3
    assert response.data["banners"][0]["title"].startswith("Banner")


@pytest.mark.django_db
def test_home_page_view_with_recent_news(client, create_recent_news):
    """Test the home page view with recent news."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["news"]) == 5
    assert response.data["news"][0]["title"].startswith("Recent News")


@pytest.mark.django_db
def test_home_page_view_with_recent_and_additional_news(
    client, create_recent_news, create_additional_news
):
    """Test the home page view with recent news and additional old news."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["news"]) == 10  # 5 recent + 5 additional
    assert (
        "Recent News" in response.data["news"][0]["title"]
        or "Old News" in response.data["news"][0]["title"]
    )


@pytest.mark.django_db
def test_home_page_view_with_recent_events(client, create_recent_events):
    """Test the home page view with recent events."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["events"]) == 5
    assert response.data["events"][0]["title"].startswith("Recent Event")


@pytest.mark.django_db
def test_home_page_view_with_recent_and_additional_events(
    client, create_recent_events, create_additional_events
):
    """Test the home page view with recent events and additional old events."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["events"]) == 10  # 5 recent + 5 additional
    assert (
        "Recent Event" in response.data["events"][0]["title"]
        or "Old Event" in response.data["events"][0]["title"]
    )


@pytest.mark.django_db
def test_home_page_view_response_structure(
    client, create_banners, create_recent_news, create_recent_events
):
    """Test the structure of the home page view response."""
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert "banners" in response.data
    assert "news" in response.data
    assert "events" in response.data
    assert isinstance(response.data["banners"], list)
    assert isinstance(response.data["news"], list)
    assert isinstance(response.data["events"], list)
