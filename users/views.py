from sqlite3 import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
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
@permission_classes([IsAuthenticated])
def get_user(request,pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        serializer1 = UserSerializer(user)

        try:
            serializer2 = UserProfileSerializer(user.userprofile)
        except UserProfile.DoesNotExist:
            profile_created = UserProfile.objects.create(user=user)
            serializer2 = UserProfileSerializer(profile_created,many=True)

        Serializer_list = [serializer1.data, serializer2.data]

        
        return Response(Serializer_list)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_update(request,pk):
    if request.method == "POST":
        user = User.objects.get(pk=pk)
        
        serializer1 = UserSerializer(instance = user, data = request.data)
        serializer2 = UserProfileSerializer(instance = user.userprofile, data = request.data)

        if serializer1.is_valid() and serializer2.is_valid():
            serializer1.save()
            serializer2.save()
        
        Serializer_list = [serializer1.data, serializer2.data]

     
        return Response(Serializer_list)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request,pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        serializer = FavoriteSerializer(user.userprofile)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorites(request,pk):
    if request.method == "POST":
        user = User.objects.get(pk=pk)
        try:
            user.userprofile.favorites.add(Recipe.objects.get(pk=request.data['id']))
        except Recipe.DoesNotExist:
            return Response({"message":"Recipe isn't found"},status=status.HTTP_400_BAD_REQUEST)

        user.userprofile.save()
        return Response({"message":"success"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_favorites(request,pk):
    if request.method == "POST":
        user = User.objects.get(pk=pk)
        try:
            user.userprofile.favorites.remove(Recipe.objects.get(pk=request.data['id']))
        except Recipe.DoesNotExist:
            return Response({"message":"Recipe isn't found"},status=status.HTTP_400_BAD_REQUEST)
    
        user.userprofile.save()
        return Response({"message":"success"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request,pk):
    if request.method == "DELETE":
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message":"success"})






