from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    favorites = serializers.SerializerMethodField(source="favorites")

    def get_favorites(self, instance):
        data = {"id": [x.id for x in instance.favorites.all()], 
        "name": [x.name for x in instance.favorites.all()],
        "name_in_arabic": [x.name_in_arabic for x in instance.favorites.all()],
        "imageURL": [x.imageURL.path for x in instance.favorites.all()],

        }

        return data

    class Meta:
        model = UserProfile
        fields = ['patient','isVegan','favorites']



