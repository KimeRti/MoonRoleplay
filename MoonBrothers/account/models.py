from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    community_rank = models.CharField(max_length=100, null=True, blank=True)
