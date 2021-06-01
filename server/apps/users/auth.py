from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed, InvalidToken,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


class AuthBackend(BaseBackend):
    def authenticate(
        self,
        _,
        username: str=None,
        password: str=None
    ) -> Optional[User]:

        UserModel = get_user_model()

        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            make_password(password, settings.SECRET_KEY)
        else:
            if user.password == make_password(password, settings.SECRET_KEY):
                return user


class JWTAuth(JWTAuthentication):
    def get_user(self, validated_token: AccessToken) -> User:
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user = self.user_model.objects.get(
                **{api_settings.USER_ID_FIELD: user_id}
            )
        except KeyError:
            raise InvalidToken(
                'Token contained no recognizable user identification'
            )
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        return user