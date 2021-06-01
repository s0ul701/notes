from typing import Dict, OrderedDict

from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Note
        fields = ('user', 'headline', 'text')
