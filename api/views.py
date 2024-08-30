from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from detection.services import detect_objects
from rest_framework import generics
from .models import UserProfile, FavoriteRecipe
from .serializers import UserProfileSerializer, FavoriteRecipeSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

class ProductDetectionView(APIView):
    def post(self, request, *args, **kwargs):
        image_data = request.data.get('image')

        if not image_data:
            print("No image provided.")
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("Received image data.")
            detected_products = detect_objects(image_data)
            print("Detected products:", detected_products)
            return Response(detected_products, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error processing image:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_user(request):
    first_name = request.data.get('first_name')
    birth_date = request.data.get('birth_date')
    preferred_cuisines = request.data.get('preferred_cuisines')

    user = User.objects.create(username=first_name)
    user_profile = UserProfile.objects.create(
        first_name=first_name,
        birth_date=birth_date,
        preferred_cuisines=preferred_cuisines
    )

    return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_profile.first_name = request.data.get('first_name', user_profile.name)
    user_profile.birth_date = request.data.get('birth_date', user_profile.birth_date)
    user_profile.preferred_cuisines = request.data.get('preferred_cuisines', user_profile.preferred_cuisines)
    user_profile.save()

    return JsonResponse({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_favorite_recipe(request):
    user_id = request.data.get('user_id')
    title = request.data.get('title')
    ingredients = request.data.get('ingredients')
    preparation = request.data.get('preparation')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    favorite_recipe = FavoriteRecipe.objects.create(
        user=user,
        title=title,
        ingredients=ingredients,
        preparation=preparation
    )

    return JsonResponse({'message': 'Recipe saved as favorite'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        user_profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user_profile)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_favorite_recipes(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    favorite_recipes = FavoriteRecipe.objects.filter(user=user)
    serializer = FavoriteRecipeSerializer(favorite_recipes, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_users(request):
    try:
        users = UserProfile.objects.all()
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)