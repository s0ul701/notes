from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Note, Tag
from .permissions import IsAuthenticatedOrOwner
from .serializers import NoteSerializer, TagSerializer
from .services import NoteServices


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrOwner,)
    serializer_class = NoteSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('headline', 'text', 'tags__name')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    @action(detail=False, url_path='notifications')
    def get_notifications(self, _: Request) -> Response:
        return NoteServices.get_notifications(
            self.get_queryset(),
            self.get_serializer,
        )


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrOwner,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
