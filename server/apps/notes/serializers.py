from typing import Dict, OrderedDict

from rest_framework import serializers, validators

from .models import Note, Tag
from .services import NoteServices


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
    )

    extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data: Dict) -> Note:
        return NoteServices.create_note_with_tags(validated_data)

    def to_representation(self, note: Note) -> OrderedDict:
        return NoteServices.to_representation(note, super().to_representation)

    class Meta:
        model = Note
        fields = ('id', 'user', 'headline', 'text', 'tags', 'start_at')


class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    extra_kwargs = {'id': {'read_only': True}}

    class Meta:
        model = Tag
        fields = ('id', 'user', 'name')
        validators = (
            validators.UniqueTogetherValidator(
                Tag.objects.all(),
                fields=('user', 'name'),
            ),
        )
