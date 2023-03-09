from api.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import base64
import six
import uuid
from users.models import *
from django.utils.translation import gettext_lazy as _

class RecipeSerializer(serializers.ModelSerializer):
    ingridents = serializers.SerializerMethodField(source="ingridents")
    
    directions = serializers.SerializerMethodField(source="directions")

    patient = serializers.SerializerMethodField(source="patient.name")

    difficulty = serializers.SerializerMethodField(source="difficulty.name")

    class Meta: 
        model = Recipe
        fields = ['id','name','ingridents','directions','patient','difficulty','time_taken','isVegetarian','created_at'] 

    def get_ingridents(self, instance):
        ig = instance.ingridents.splitlines()
        x = [x for x in ig if x]
        return x
    
    def get_directions(self, instance):
        dr = instance.directions.splitlines()
        x = [x for x in dr if x]
        return x

    def get_patient(self, instance):
        return instance.patient.name
    
    def get_difficulty(self, instance):
        return instance.difficulty.name
   

class PatientSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Patient
        fields = '__all__' 

class ErrorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Error
        fields = '__all__'
