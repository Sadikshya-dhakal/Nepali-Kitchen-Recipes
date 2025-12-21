from django.urls import path
from recipes import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("categories/", views.AllCategoriesView.as_view(), name="all-categories"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
]