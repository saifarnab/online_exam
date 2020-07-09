from django.db import models
from auth_user.models import Profile


class Paper(models.Model):
    paper_id = models.BigAutoField(primary_key=True)
    paper_name = models.CharField(max_length=500, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    start_time = models.CharField(max_length=50, null=False, blank=False)
    end_time = models.CharField(max_length=50, null=False, blank=False)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    question_id = models.BigIntegerField()
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)
    question = models.TextField(null=False, blank=False)
    choice = models.CharField(max_length=50, null=False, blank=False)
    answer = models.CharField(max_length=50, null=False, blank=False)
