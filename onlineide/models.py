from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# get rid of this model as we are using inbuilt user model provided by djamgo
# class User(models.Model):
#     fullname = models.CharField(max_length=100)


class SubmissionCode(models.Model):
    # choices we have for acceptance
    ACCEPTANCE_STATUS = [
        ("S", "Success"),
        ("P", "Pending"),
        ("E", "Error")
    ]
    code = models.CharField(max_length=2000)
    language = models.CharField(max_length=100)
    submission_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=ACCEPTANCE_STATUS)
    user_input = models.CharField(max_length=200, null=True, blank=True)
    user_output = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
