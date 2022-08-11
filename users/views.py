import json
from sqlite3 import IntegrityError
from django.shortcuts import render
from api.serializers import RecipeSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from users.serailizers import *
from rest_framework.response import Response
from django.contrib.auth import login
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import status
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.mail import send_mail  
from django.dispatch import receiver



# Register User
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        print("This Email " + serializer.validated_data['email'])

        emailExist = User.objects.filter(email = email).exists()

    

        if emailExist:
            return Response(
                {
                'email' : "This email already exists"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        else:
            user = serializer.save()
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })
            

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            login(request, user)
        except:
            UserProfile.objects.create(user=user)

        temp_list=super(LoginAPI, self).post(request, format=None)
        temp_list.data['user_id'] = user.id 
        return Response({"data":temp_list.data})



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    msg = "Your code is ".format(reset_password_token.key)

    send_mail(
        # title:
        "Reset Password | Livine ",
        # message:
        msg,
        # from:
        "pristineguava@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    if request.method == "GET":
        
        user = request.user
        if user.is_authenticated:
            try:
                
                serializer1 = UserSerializer(user)
                serializer2 = UserProfileSerializer(user.userprofile)
            except UserProfile.DoesNotExist:

                profile_created = UserProfile.objects.create(user=user)
                serializer2 = UserProfileSerializer(profile_created,many=True)
        else:
            guest_data = {
                "id": 0,
                "username": "GUEST",
                "email": "",
            }
            return Response(guest_data)
        

        Serializer_list = [serializer1.data, serializer2.data]
        new = {}
        for d in Serializer_list:
            new.update(d)
        
        return Response(new)


@api_view(['POST'])
def user_update(request):
    if request.method == "POST":
        user = request.user
        
        serializer1 = UserSerializer(instance = user, data = request.data)
        serializer2 = UserProfileSerializer(instance = user.userprofile, data = request.data)

        if serializer1.is_valid():
            serializer1.save()
        
        if serializer2.is_valid():
            serializer2.save()
        
        Serializer_list = [serializer1.data, serializer2.data]

        new = {}
        for d in Serializer_list:
            new.update(d)
        
        return Response(new)

@api_view(['GET'])
def get_favorites(request):
    if request.method == "GET":
        user = request.user
        serializer = FavoriteSerializer(user.userprofile)
        return Response(serializer.data)

@api_view(['POST'])
def add_favorites(request):
    if request.method == "POST":
        user = request.user
        try:
            user.userprofile.favorites.add(Recipe.objects.get(pk=request.data['id']))
        except Recipe.DoesNotExist:
            return Response({"message":"Recipe isn't found"},status=status.HTTP_400_BAD_REQUEST)

        user.userprofile.save()
        return Response({"message":"success"})


@api_view(['POST'])
def delete_favorites(request):
    if request.method == "POST":
        user = request.user
        try:
            user.userprofile.favorites.remove(Recipe.objects.get(pk=request.data['id']))
        except Recipe.DoesNotExist:
            return Response({"message":"Recipe isn't found"},status=status.HTTP_400_BAD_REQUEST)
    
        user.userprofile.save()
        return Response({"message":"success"})


@api_view(['DELETE'])
def delete_account(request):
    if request.method == "DELETE":
        user = request.user
        user.delete()
        return Response({"message":"success"})





@api_view(['GET'])
def get_user_veg_status(request):
    if request.method == "GET":
        user = request.user
        try:
            return Response(user.userprofile.isVegan)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)
            return Response(user.userprofile.isVegan)





