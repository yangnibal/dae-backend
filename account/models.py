from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    password  = models.CharField(max_length=50)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=11)
    can_access_1 = models.BooleanField(default=False)
    can_access_2 = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'is_staff', 'name', 'phone_number', 'can_access_1', 'can_access_2']

    objects = UserManager()
