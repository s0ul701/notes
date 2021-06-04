from datetime import datetime, timedelta
from typing import Dict, OrderedDict

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.response import Response

from .models import Note


class NoteServices:
    @staticmethod
    def create_note_with_tags(note_data: Dict) -> Note:
        tags_ids = note_data.pop('tags')
        note = Note.objects.create(**note_data)
        if tags_ids:
            note.tags.set(tags_ids)
        return note

    @staticmethod
    def to_representation(note: Note, base_to_repr) -> OrderedDict:
        note_data = base_to_repr(note)
        note_data['tags'] = [{
            'id': tag.id,
            'name': tag.name,
        } for tag in note.tags.all()]
        return note_data

    @staticmethod
    def get_notifications(
        queryset: QuerySet,
        notification_serializer,
    ) -> Response:

        notes_for_notifications = queryset.filter(
            is_watched=False,
            start_at__gt=datetime.now(),
            start_at__lte=datetime.now() + timedelta(
                hours=settings.NOTIFICATION_TIME_HOURS
            ),
        )
        notifications_data = notification_serializer(
            notes_for_notifications,
            many=True,
        ).data
        notes_for_notifications.update(is_watched=True)
        return Response(notifications_data)
