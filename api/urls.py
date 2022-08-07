from django.urls import path , include
from . import views

urlpatterns = [
    path('recipe/<int:pk>', views.recipeDetail),
    path('recipe/veg/<int:pk>', views.get_veg_recipes),
    
    path('patient/<str:patient>', views.recipe_per_patient),
    path('allPatients/', views.all_patients),
    path('', include('users.urls')),

]