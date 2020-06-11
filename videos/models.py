from django.db import models
from groups.models import InfGroup

class Video(models.Model):
    name = models.CharField(max_length=20)
    link = models.TextField()
    iframe = models.TextField()
    subject = models.CharField(max_length=10)
    grade = models.CharField(max_length=5)
    group = models.ForeignKey(InfGroup, null=True, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    