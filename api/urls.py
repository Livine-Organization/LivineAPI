from django.urls import path , include
from . import views

urlpatterns = [
    path('recipe', views.home),
    path('recipe/<int:pk>', views.recipeDetail),
    path('recipe/veg/<int:pk>', views.get_veg_recipes),

    
    path('patient/<str:patient>', views.recipeTypeDetail),
    path('allPatients/', views.recipe_all_types),
    path('', include('users.urls')),

]