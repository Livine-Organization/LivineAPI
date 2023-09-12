from django.urls import path, include
from users import views
from knox import views as knox_views


urlpatterns = [
     path('register/', views.RegisterAPI.as_view(), name='register'),
    path('user/', views.get_user, name='Users'),
    path('user/delete/', views.delete_account, name='Delete Account'),

    path('user/update/', views.user_update, name='UsersUpdate'),

    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



    path('user/favorite/', views.get_favorites, name='Display Favorites'),
    path('addfavorite/', views.add_favorites, name='Add Favorites'),
    path('deletefavorite/', views.delete_favorites, name='Delete Favorites'),

    path('user/update/points/', views.update_points, name='Update points'),



]