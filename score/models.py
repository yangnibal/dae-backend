from django.db import models
from tests.models import Test
from students.models import Student
from account.models import User

class Score(models.Model):
    score = models.CharField(max_length=10)
    percent = models.CharField(max_length=7)
    rank = models.CharField(max_length=5)
    rating = models.CharField(max_length=2)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    prob_dens = models.CharField(max_length=10)
    z = models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)
