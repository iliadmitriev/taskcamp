"""
Accounts models module.

Contains:

    class UserManager: model manager for model User
    class User: model for User

"""

from typing import Optional

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field.

    Attributes:
        use_in_migrations: model can be altered by migration.

    """

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> AbstractUser:
        """Create and save a User with the given email and password.

        Args:
            email (str): user email.
            password (str): user password
            **extra_fields: user extra information

        Returns:
            (AbstractUser): created user from database

        Raises:
            ValueError: if bad data provided.

        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> AbstractUser:
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> AbstractUser:
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Redefined User model.

    `Username` field removed.
    `Email` field used as identifier.
    Added field `birthdate`

    Redefined manager `UserManager`
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)

    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
