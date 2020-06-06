from django.db import models
from account.models import User

class Group(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class InfGroup(models.Model):
    name = models.CharField(max_length=20)
    