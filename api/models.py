
from django.db import models

from .compress_image import compress
from django.utils.translation import gettext as _

class Patient(models.Model):
    name = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='patients', null=True)

    def __str__(self):
        return self.name

class Difficulty(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='difficulties', null=True)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    imageURL = models.ImageField(upload_to='recipes', null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    isVegetarian = models.BooleanField(default=False)
    time_taken = models.IntegerField(null=True)
    calories = models.IntegerField(null=True)
    video = models.CharField(max_length=500, null=True)
    ingridents = models.TextField(default="")
    directions = models.TextField(default="")
    
    created_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        new_image = compress(self.imageURL)
        # set self.image to new_image
        self.imageURL = new_image
        # save
        super().save(*args, **kwargs)

        
    def __str__(self):
        return self.name


class Error(models.Model):
    model = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    device_version = models.CharField(max_length=100,default="")
    error = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.error




    





