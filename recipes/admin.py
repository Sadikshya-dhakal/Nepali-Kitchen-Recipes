from django.contrib import admin
from .models import Advertisement, Category, Recipe, Newsletter, AboutPage, CoreValue, OurTeam, Contact, NewsletterSubscription
from django import forms
from tinymce.widgets import TinyMCE


# Register your models here.

admin.site.register(Newsletter)
admin.site.register(AboutPage)
admin.site.register(CoreValue)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(Advertisement) 
admin.site.register(NewsletterSubscription)

class RecipeAdminForm(forms.ModelForm):
    chef_tips = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}), required=False)
    
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ['title', 'author', 'category', 'status', 'difficulty', 'published_at']
    list_filter = ['status', 'difficulty', 'category', 'is_featured']
    search_fields = ['title', 'description']

admin.site.register(Recipe, RecipeAdmin)


