
from django.db import models

from .compress_image import compress

class Patient(models.Model):
    name = models.CharField(max_length=100,null=True)
    name_in_arabic = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    diff_list = (("Easy","Easy"),("Medium","Medium"),("Hard","Hard"))

    name = models.CharField(max_length=50)

    name_in_arabic= models.CharField(max_length=50,default='')

    imageURL = models.ImageField(upload_to='recipes', null=True)

    diff = models.CharField(max_length=10, choices=diff_list, default="Easy")

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    isVegetarian = models.BooleanField(default=False)

    time_taken = models.IntegerField(null=True)

    calories = models.IntegerField(null=True)

    video = models.CharField(max_length=500, null=True)

    video_in_arabic = models.CharField(max_length=500, null=True)

    ingridents = models.TextField(default="")

    ingridents_in_arabic = models.TextField(default="")
    
    
    directions = models.TextField(default="")
    
    directions_in_arabic = models.TextField(default="")

    created_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        new_image = compress(self.imageURL)
        # set self.image to new_image
        self.imageURL = new_image
        # save
        super().save(*args, **kwargs)

        
    def __str__(self):
        return self.name




    





