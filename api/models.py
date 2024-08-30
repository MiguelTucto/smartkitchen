from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    preferred_cuisines = models.TextField()

    def __str__(self):
        return self.first_name

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    ingredients = models.TextField(max_length=1000)
    preparation = models.TextField(max_length=1000)

    def __str__(self):
        return self.title
