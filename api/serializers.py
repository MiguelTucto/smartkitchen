from rest_framework import serializers
from .models import UserProfile, FavoriteRecipe

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'user_id', 'title', 'ingredients', 'preparation']

class UserProfileSerializer(serializers.ModelSerializer):
    favorite_recipes = FavoriteRecipeSerializer(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'birth_date', 'preferred_cuisines', 'favorite_recipes']

    def create(self, validated_data):
        favorite_recipes_data = validated_data.pop('favorite_recipes', [])
        user_profile = UserProfile.objects.create(**validated_data)

        for recipe_data in favorite_recipes_data:
            FavoriteRecipe.objects.create(user=user_profile, **recipe_data)

        return user_profile

    def update(self, instance, validated_data):
        favorite_recipes_data = validated_data.pop('favorite_recipes', [])

        instance.first_name = validated_data.get('first_name', instance.name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.preferred_cuisines = validated_data.get('preferred_cuisines', instance.preferred_cuisines)
        instance.save()

        for recipe_data in favorite_recipes_data:
            recipe_id = recipe_data.get('id')
            if recipe_id:
                recipe = FavoriteRecipe.objects.get(id=recipe_id, user_profile=instance)
                recipe.title = recipe_data.get('title', recipe.title)
                recipe.ingredients = recipe_data.get('ingredients', recipe.ingredients)
                recipe.preparations = recipe_data.get('preparations', recipe.preparations)
                recipe.save()
            else:
                FavoriteRecipe.objects.create(user=instance, **recipe_data)

        return instance
