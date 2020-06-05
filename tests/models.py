from django.db import models
from students.models import Student
from account.models import User

class Test(models.Model):
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
    TESTTYPE_CHOICES = (
        ("1학기 중간", "1학기 중간"),
        ("1학기 기말", "1학기 기말"),
        ("2학기 중간", "2학기 중간"),
        ("2학기 기말", "2학기 기말"),
        ("3월 모의고사", "3월 모의고사"),
        ("6월 모의고사", "6월 모의고사"),
        ("9월 모의고사", "9월 모의고사"),
        ("11월 모의고사", "11월 모의고사"),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    test_type = models.CharField(max_length=10, choices=TESTTYPE_CHOICES)
    subject = models.CharField(max_length=10)
    average = models.CharField(max_length=10)
    std_dev = models.CharField(max_length=20)
    cand_num = models.CharField(max_length=20)
    additional_info = models.TextField()
    student = models.ManyToManyField(Student, default=None)
    id = models.AutoField(primary_key=True)

