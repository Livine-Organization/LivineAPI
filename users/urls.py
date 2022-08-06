from django.urls import path, include
from users import views
from knox import views as knox_views


urlpatterns = [
     path('register/', views.RegisterAPI.as_view(), name='register'),
    path('user/<int:pk>/', views.get_user, name='Users'),
    path('user/delete/<int:pk>/', views.delete_account, name='Delete Account'),
    path('user/veg/<int:pk>/', views.get_user_veg_status),

    path('user/update/<int:pk>/', views.user_update, name='UsersUpdate'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



    path('user/favorite/<int:pk>/', views.get_favorites, name='Display Favorites'),
    path('addfavorite/<int:pk>/', views.add_favorites, name='Add Favorites'),
    path('deletefavorite/<int:pk>/', views.delete_favorites, name='Delete Favorites'),



]