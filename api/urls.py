from django.urls import path
from .views import ProductDetectionView
from . import views

urlpatterns = [
    path('detect/', ProductDetectionView.as_view(), name='product-detection'),
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('create-favorite-recipe/', views.create_favorite_recipe, name='create_favorite_recipe'),
    path('get-user-profile/<int:user_id>/', views.get_user_profile, name='get_user_profile'),
    path('get-user-favorite-recipes/<int:user_id>/', views.get_user_favorite_recipes, name='get_user_favorite_recipes'),
    path('get-all-users/', views.get_all_users, name='get_all_users'),

]