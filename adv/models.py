from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    def __str__(self):
        return f"{self.first_name}"



class RecruiterModel(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    user = models.OneToOneField(
        UserModel,
        related_name="recruiter",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f"{self.user.last_name}"
    


class JobModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    salaty = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recruiter = models.ForeignKey(
        RecruiterModel, 
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    def __str__(self):
        return f"{self.title}"