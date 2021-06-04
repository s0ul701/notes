from datetime import datetime, timedelta

import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.notes.models import Note
from apps.users.models import User


def create_user(username: str = 'username') -> User:
    user_data = {
        'username': username,
        'password': 'password',
    }
    return User.objects.create_user(**user_data)


def api_client(user: User) -> APIClient:
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client


@pytest.mark.django_db
class TestNote:
    notes_api_url = '/api/v1/notes/'

    def test_create(self):
        user = create_user()
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
        }

        response = api_client(user).post(self.notes_api_url, data=note_data)
        created_note = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        for field in note_data:
            assert created_note[field] == note_data[field]

    def test_create_not_auth(self, client):
        response = client.post(self.notes_api_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_owner(self):
        user1 = create_user('username1')
        user2 = create_user('username2')
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
        }
        notes_quantity = 5
        Note.objects.bulk_create([
            *[Note(**note_data, user=user1) for _ in range(notes_quantity)],
            *[Note(**note_data, user=user2) for _ in range(notes_quantity)],
        ])

        response1 = api_client(user1).get(self.notes_api_url)
        response2 = api_client(user2).get(self.notes_api_url)

        assert response1.status_code == status.HTTP_200_OK
        assert len(response1.data) == notes_quantity
        assert response2.status_code == status.HTTP_200_OK
        assert len(response2.data) == notes_quantity

    def test_update_owner(self):
        user = create_user()
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
            'user': user,
        }
        note = Note.objects.create(**note_data)
        updating_data = {
            'headline': 'New Headline',
            'text': 'New Text',
        }

        response = api_client(user).patch(
            f'{self.notes_api_url}{note.id}/',
            updating_data,
        )
        updating_note = response.json()

        assert response.status_code == status.HTTP_200_OK
        for field in updating_data:
            assert updating_note[field] == updating_data[field]

    def test_update_not_owner(self):
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
            'user': create_user('username1'),
        }
        note = Note.objects.create(**note_data)

        response = api_client(create_user('username2')).patch(
            f'{self.notes_api_url}{note.id}/',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_owner(self):
        user = create_user()
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
            'user': user,
        }
        note = Note.objects.create(**note_data)

        response = api_client(user).delete(f'{self.notes_api_url}{note.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_owner(self):
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
            'user': create_user('username1'),
        }
        note = Note.objects.create(**note_data)
        client = api_client(create_user('username2'))

        response = client.delete(f'{self.notes_api_url}{note.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_notifications(self):
        user = create_user()
        note_data = {
            'headline': 'Headline',
            'text': 'Text',
        }
        Note.objects.create(
            user=user,
            start_at=datetime.now() - timedelta(hours=1),
            **note_data,
        )
        Note.objects.create(
            user=user,
            start_at=datetime.now() + timedelta(
                hours=settings.NOTIFICATION_TIME_HOURS + 1,
            ),
            **note_data,
        )
        note = Note.objects.create(
            user=user,
            start_at=datetime.now() + timedelta(
                hours=settings.NOTIFICATION_TIME_HOURS - 1,
            ),
            **note_data,
        )

        response = api_client(user).get(f'{self.notes_api_url}notifications/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == note.id
