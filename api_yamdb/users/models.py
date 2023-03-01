from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)


class User(AbstractUser):
    """Model User от AbstractUser."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        default=False
    )
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=256,
        null=True,
        editable=False,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=USER_ROLES,
        default=USER
    )

    class Meta:
        """Класс Meta."""

        ordering = ['-date_joined']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='not_me'
            )
        ]

    def __str__(self):
        """Возвращает username."""
        return self.username

    @property
    def is_admin(self):
        """."""
        return (
            self.role == User.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """."""
        return self.role == User.MODERATOR
