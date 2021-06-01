from djongo import models

from .managers import CustomUserManager


class User(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Username',
    )
    password = models.CharField(max_length=128, verbose_name='Password')

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
