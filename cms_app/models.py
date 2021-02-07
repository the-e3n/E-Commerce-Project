from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Sagar',
            last_name='s'

        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name='Username')
    first_name = models.CharField(max_length=100, default='First Name')
    last_name = models.CharField(max_length=100, default='Last Name')
    is_admin = models.BooleanField(default=False)
    email = models.CharField(max_length=200,)
    objects = UserManager()

    def __str__(self):
        return self.username
