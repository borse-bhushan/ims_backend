import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAuth:
    def setup_method(self, authenticated_client):
        self.client = APIClient()

    def test_super_admin_login(self, au):
        payload = {"username": "borsebhushan216@gmail.com", "password": "1234"}
        response = self.client.post("/auth/admin/login", payload, format="json")
        assert response.status_code == 201
        assert "token" in response.data["data"]
