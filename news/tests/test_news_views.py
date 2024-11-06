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
        "image": None,  # valid image file can be used for tests.
    }


@pytest.mark.django_db
class TestNewsFeed:
    def test_create_news(self, client, news_data):
        url = reverse("newsfeed-list-create")
        response = client.post(url, news_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == news_data["title"]
        assert response.data["description"] == news_data["description"]

    def test_retrieve_news_list(self, client, news_data):
        client.post(reverse("newsfeed-list-create"), news_data, format="json")

        url = reverse("newsfeed-list-create")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_specific_news(self, client, news_data):
        create_response = client.post(
            reverse("newsfeed-list-create"), news_data, format="json"
        )
        news_id = create_response.data["id"]

        url = reverse("newsfeed-detail", args=[news_id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == news_data["title"]

    def test_update_news(self, client, news_data):
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
        create_response = client.post(
            reverse("newsfeed-list-create"), news_data, format="json"
        )
        news_id = create_response.data["id"]

        url = reverse("newsfeed-detail", args=[news_id])
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = client.get(url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthorized_access(self, client, news_data):
        url = reverse("newsfeed-list-create")
        client.post(url, news_data, format="json")

        # assert response.status_code == status.HTTP_403_FORBIDDEN  # activate when permission is required
