from django.urls import path
from recipes import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("categories/", views.AllCategoriesView.as_view(), name="all-categories"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("recipes/", views.AllRecipesView.as_view(), name="all-recipes"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
    path('newsletter/subscribe/', views.NewsletterSubscriptionView.as_view(), name='newsletter-subscribe'),
    path("search/", views.RecipeSearchView.as_view(), name="search"),
]