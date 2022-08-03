from django.db import models
from django.contrib.auth.models import User
from api.models import *

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    isVegan = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username + " Profile"
