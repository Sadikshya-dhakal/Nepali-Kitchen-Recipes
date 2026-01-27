from django.contrib.auth.models import Group, User
from rest_framework import serializers

from recipes.models import Category, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "image",
            "description",
            "gradient_from",
            "gradient_to",
            "order",
            "recipe_count",
        ]
        extra_kwargs = {
            "recipe_count": {"read_only": True},
        }
    
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "content",
            "featured_image",
            "status",
            "category",
            "prep_time",
            "cook_time",
            "servings",
            "difficulty",
            "ingredients",
            "instructions",
            "chef_tips",
            "is_trending",
            "is_featured",
            # read only
            "author",
            "views_count",
            "likes_count",
            "rating",
            "review_count",
            "published_at",
        ]
        extra_kwargs = {
            "author": {"read_only": True},
            "views_count": {"read_only": True},
            "likes_count": {"read_only": True},
            "rating": {"read_only": True},
            "review_count": {"read_only": True},
            "published_at": {"read_only": True},
        }
    
    def validate(self, data):
        data["author"] = self.context["request"].user
        return data