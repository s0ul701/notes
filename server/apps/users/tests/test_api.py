import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUser:
    users_api_url = '/api/v1/users/'

    def test_create(self, client):
        user_data = {
            'username': 'username',
            'password': 'password',
            'password_confirmation': 'password'
        }

        response = client.post(self.users_api_url, data=user_data)
        created_user = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        for field in created_user:
            assert user_data[field] == created_user[field]
