from django.contrib.auth.hashers import make_password
from djongo.models import DjongoManager
from django.conf import settings


class CustomUserManager(DjongoManager):
    def create_user(self, username: str, password: str):
        user = self.model(
            username=username,
            password=make_password(password, settings.SECRET_KEY),
        )
        user.save()
        return user
