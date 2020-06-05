from django.db import models
from groups.models import Group
from account.models import User

class Student(models.Model):
    GRADE_CHOICES = (
        ("초1", "초1"),
        ("초2", "초2"),
        ("초3", "초3"),
        ("초4", "초4"),
        ("초5", "초5"),
        ("초6", "초6"),
        ("중1", "중1"),
        ("중2", "중2"),
        ("중3", "중3"),
        ("고1", "고1"),
        ("고2", "고2"),
        ("고3", "고3")
    )
    name = models.CharField(max_length=5)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)