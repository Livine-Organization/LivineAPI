from api.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import base64
import six
import uuid
from users.models import *

class RecipeSerializer(serializers.ModelSerializer):
    ingridents = serializers.SerializerMethodField(source="ingridents")
    ingridents_in_arabic = serializers.SerializerMethodField(source="ingridents_in_arabic")
    
    directions = serializers.SerializerMethodField(source="directions")

    patient = serializers.SerializerMethodField(source="patient.name")

    patient_in_arabic = serializers.SerializerMethodField(source="patient.name_in_arabic")

    directions_in_arabic = serializers.SerializerMethodField(source="directions_in_arabic")


    def get_ingridents(self, instance):
        ig = instance.ingridents.splitlines()
        x = [x for x in ig if x]
        return x

    def get_ingridents_in_arabic(self, instance):
        ig_a = instance.ingridents_in_arabic.splitlines()
        x = [x for x in ig_a if x]
        return x
    
    def get_directions(self, instance):
        dr = instance.directions.splitlines()
        x = [x for x in dr if x]
        return x

    def get_directions_in_arabic(self, instance):
        dr_a = instance.directions_in_arabic.splitlines()
        x = [x for x in dr_a if x]
        return x

    def get_patient(self, instance):
        return instance.patient.name
    
    def get_patient_in_arabic(self, instance):
        return instance.patient.name_in_arabic


    
    class Meta: 
        model = Recipe
        fields = '__all__' 


class PatientSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Patient
        fields = '__all__' 
