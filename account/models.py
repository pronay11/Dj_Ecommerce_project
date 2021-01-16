from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    photo = models.ImageField(default="john-doe.jpg")
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username