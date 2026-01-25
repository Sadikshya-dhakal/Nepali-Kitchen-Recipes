from django.contrib.auth.models import Group, User
from rest_framework import serializers

from recipes.models import Category


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
    
