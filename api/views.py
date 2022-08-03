from api.models import Recipe
from api.serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response



def index(request):
    return render(request, 'api/index.html')

@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        recipe = Recipe.objects.all()
        serializer = RecipeSerializer(recipe, many=True)
        
        return Response(serializer.data)



@api_view(['GET'])
def recipeDetail(request,pk):
    if request.method == "GET":
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(recipe)
    
        return Response(serializer.data)




@api_view(['GET'])
def recipeTypeDetail(request,patient):
    if request.method == "GET":
        recipe = Recipe.objects.filter(patient=patient).order_by('-created_at')
        serializer = RecipeSerializer(recipe,many=True)

        return Response(serializer.data)


@api_view(['GET'])
def recipe_all_types(request):
    if request.method == "GET":
        recipe = Patient.objects.all()
        serializer = PatientSerializer(recipe,many=True)
        return Response(serializer.data)




