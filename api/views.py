from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.serializers import CategorySerializer, GroupSerializer, RecipePublishSerializer, RecipeSerializer, UserSerializer
from recipes.models import Category, Recipe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by("order", "name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        
        return super().get_permissions()
    
class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by("-published_at")
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.filter(status="active", published_at__isnull=False)
            
            query = self.request.query_params.get("query", None)
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
        
        return queryset
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()
    

class DraftListView(ListAPIView):
    queryset = Recipe.objects.filter(published_at__isnull=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

class DraftDetailView(RetrieveAPIView):
    queryset = Recipe.objects.filter(published_at__isnull=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecipePublishViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = RecipePublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            recipe = Recipe.objects.get(pk=data["id"])
            recipe.published_at = timezone.now()
            recipe.status = "active"
            recipe.save()
            serialized_data = RecipeSerializer(recipe).data
            return Response(serialized_data, status=status.HTTP_200_OK)