from api.models import Recipe
from api.serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
import os
def index(request):
    return render(request, 'api/index.html')


class VegRecipeListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name_en','name_ar','ingridents_en','ingridents_ar']
    def get_queryset(self):
        queryset = Recipe.objects.filter(isVegetarian=True,patient=self.kwargs['pk']).order_by('-created_at')
        return queryset

class RecipeListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecipeSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ['name_en','name_ar','ingridents_en','ingridents_ar']
    def get_queryset(self):
        queryset = Recipe.objects.filter(patient=self.kwargs['patient']).order_by('-created_at')    
        return queryset

@api_view(['GET'])
@permission_classes([AllowAny])
def recipeDetail(request,pk):
    if request.method == "GET":
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(recipe)

    
        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def all_patients(request):
    if request.method == "GET":
        recipe = Patient.objects.all()
        serializer = PatientSerializer(recipe,many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def errors(request):
    if request.method == "POST":
        serializer = ErrorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)   



@api_view(['POST'])
@permission_classes([AllowAny])
def update(request):
    latest_version = "8.5.5"
    media_url = "http://"+request.META['HTTP_HOST']+"/media/apk/"
    hardware = request.data['hardware']
    download_url = media_url+ "app-armeabi-v7a-release.apk"
    if "v7a" in hardware:
        download_url = media_url+ "app-armeabi-v7a-release.apk"
    elif "v8a" in hardware:
        download_url = media_url+ "app-arm64-v8a-release.apk"
    elif "x86" in hardware:
        download_url = media_url+ "app-x86_64-release.apk"

    return Response({"latest_version":latest_version,"download_url":download_url})
    


