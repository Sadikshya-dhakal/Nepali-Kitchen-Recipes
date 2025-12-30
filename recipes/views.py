from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q, Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from recipes.forms import ContactForm
from .models import Contact, Newsletter, Recipe, Category, AboutPage, CoreValue, OurTeam, Review


class HomeView(TemplateView):
    template_name = "recipes/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories
        context["categories"] = Category.objects.all()
        
        # Get trending recipes
        context["trending_recipes"] = Recipe.objects.filter(
            published_at__isnull=False, 
            status="active", 
            is_trending=True
        ).order_by("-published_at")[:6]
        
        return context


class AllCategoriesView(ListView):
    model = Category
    template_name = "recipes/category/all_categories.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        return Category.objects.all().order_by('order', 'name')


class CategoryDetailView(ListView):
    model = Recipe
    template_name = "recipes/category/category.html"
    context_object_name = "recipes"
    paginate_by = 1
    
    def get_queryset(self):
        return Recipe.objects.filter(
            category__pk=self.kwargs.get('pk'),
            published_at__isnull=False,
            status="active"
        ).order_by("-published_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs.get('pk'))
        
        # Add related categories (exclude current category)
        context['related_categories'] = Category.objects.exclude(
            pk=self.kwargs.get('pk')
        ).annotate(
            total_recipes=Count('recipes', filter=Q(recipes__status='active'))
        )[:6]
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/category/detail/recipe_detail.html"
    context_object_name = "recipe"
    
    def get_queryset(self):
        return Recipe.objects.filter(
            published_at__isnull=False, 
            status="active"
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stars"] = range(5)
        
        # Increment views
        current_recipe = self.object
        current_recipe.views_count += 1
        current_recipe.save()
        
        # Related recipes
        context["related_recipes"] = (
            Recipe.objects.filter(
                published_at__isnull=False,
                status="active",
                category=self.object.category,
            )
            .exclude(id=self.object.id)
            .order_by("-published_at")[:3]
        )
        
        return context
    
class AboutView(TemplateView):
    template_name = "recipes/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get about page content
        context['about_page'] = AboutPage.objects.first()
        
        # Get core values
        context['core_values'] = CoreValue.objects.all()
        
        
        # Get team members
        context['team_members'] = OurTeam.objects.all()

         # Calculate dynamic statistics (auto-updating)
        context['active_users_count'] = Newsletter.objects.filter(is_active=True).count()
        context['total_recipes_count'] = Recipe.objects.filter(status='active').count()
        context['total_reviews_count'] = Review.objects.filter(is_approved=True).count()
        context['total_categories_count'] = Category.objects.count()
        
        return context

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "recipes/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error sending your message. Please check the form.",
        )
        return super().form_invalid(form)