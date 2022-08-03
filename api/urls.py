from django.urls import path , include
from . import views

urlpatterns = [
    path('recipe', views.home),

    
    path('patient/<str:patient>', views.recipeTypeDetail),
    path('allPatients/', views.recipe_all_types),
    path('', include('users.urls')),

   

]