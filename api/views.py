from multiprocessing import context
from api.models import Recipe
from api.serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

def index(request):
    return render(request, 'api/index.html')


@api_view(['GET'])
def recipeDetail(request,pk):
    if request.method == "GET":
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(recipe)
    
        return Response(serializer.data)




@api_view(['GET'])
def recipe_per_patient(request,patient):
    if request.method == "GET":
        recipe = Recipe.objects.filter(patient=patient).order_by('-created_at')
        serializer = RecipeSerializer(recipe,many=True)

        return Response(serializer.data,content_type='application/json;charset=UTF-8')


@api_view(['GET'])
def all_patients(request):
    if request.method == "GET":
        recipe = Patient.objects.all()
        serializer = PatientSerializer(recipe,many=True)
        return Response(serializer.data)



@api_view(['GET'])
def get_veg_recipes(request,pk):
    if request.method == "GET":
        recipes = Recipe.objects.filter(isVegetarian=True,patient=pk)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data,content_type='application/json;charset=UTF-8')
    


class RecipeListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ['name','name_in_arabic','ingridents','ingridents_in_arabic']
