from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Category, Recipe

# Create your views here.


class HomeView(TemplateView):
    template_name = "recipes/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get 6 categories for "Explore Nepal's Culinary Heritage" section
        context["categories"] = Category.objects.all()[:6]
        
        # Get 4 trending recipes for "Trending Now" section
        context["trending_recipes"] = Recipe.objects.filter(
            published_at__isnull=False, 
            status="active", 
            is_trending=True
        ).order_by("-published_at")[:6]
        
        return context