from django.db import models
from account.models import User

class Group(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

class InfGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    