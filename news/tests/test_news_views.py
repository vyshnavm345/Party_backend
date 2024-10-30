import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def news_data():
    return {
        "title": "Test News Title",
        "description": "This is a test news description.",
        "image": None,  # You can use a valid image file for actual tests
    }


@pytest.mark.django_db
class TestNewsFeed:
    def test_create_news(self, client, news_data):
        url = reverse(
            "newsfeed-list-create"
        )  # Ensure the URL name matches your urls.py
        response = client.post(url, news_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == news_data["title"]
        assert response.data["description"] == news_data["description"]

    def test_retrieve_news_list(self, client, news_data):
        # Create a news item first
        client.post(reverse("newsfeed-list-create"), news_data, format="json")

        url = reverse("newsfeed-list-create")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  # Ensure the list is not empty

    def test_retrieve_specific_news(self, client, news_data):
        # Create a news item first
        create_response = client.post(
            reverse("newsfeed-list-create"), news_data, format="json"
        )
        news_id = create_response.data["id"]

        url = reverse("newsfeed-detail", args=[news_id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == news_data["title"]

    def test_update_news(self, client, news_data):
        # Create a news item first
        create_response = client.post(
            reverse("newsfeed-list-create"), news_data, format="json"
        )
        news_id = create_response.data["id"]

        updated_data = {"title": "Updated Title", "description": "Updated description."}
        url = reverse("newsfeed-detail", args=[news_id])
        response = client.put(url, updated_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == updated_data["title"]

    def test_delete_news(self, client, news_data):
        # Create a news item first
        create_response = client.post(
            reverse("newsfeed-list-create"), news_data, format="json"
        )
        news_id = create_response.data["id"]

        url = reverse("newsfeed-detail", args=[news_id])
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check that the news item was deleted
        get_response = client.get(url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthorized_access(self, client, news_data):
        # Attempt to create a news article without authentication
        url = reverse("newsfeed-list-create")
        client.post(url, news_data, format="json")

        # assert response.status_code == status.HTTP_403_FORBIDDEN  # activate when permission is required
