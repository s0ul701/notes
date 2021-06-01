from typing import Dict, OrderedDict

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, user_data: OrderedDict) -> OrderedDict:
        if user_data['password'] != user_data.pop('password_confirmation'):
            raise serializers.ValidationError({
                'password_confirmation': 'Password mismatch!',
            })
        return user_data

    def create(self, validated_data: Dict):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmation')
