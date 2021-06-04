from django.conf import settings
from django.contrib.auth.hashers import make_password
from djongo.models import DjongoManager


class CustomUserManager(DjongoManager):
    def create_user(self, username: str, password: str):
        user = super().create(
            username=username,
            password=make_password(password, settings.SECRET_KEY),
        )
        return user
