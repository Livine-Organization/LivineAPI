from django.urls import path , include
from . import views

urlpatterns = [
    path('recipe/<int:pk>/', views.recipeDetail),
    path('recipe/veg/<int:pk>/', views.VegRecipeListView.as_view()),
    path('patient/<str:patient>/', views.RecipeListView.as_view()),
    path('allPatients/', views.all_patients),
    path('', include('users.urls')),
    path('errors/', views.errors),
]