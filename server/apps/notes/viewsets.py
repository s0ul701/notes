from rest_framework import viewsets

from .models import Note
from .permissions import IsAuthenticatedOrOwner
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrOwner,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
