from django.contrib import admin
from .models import Category, Recipe, Newsletter, AboutPage, CoreValue, OurTeam, Contact, NewsletterSubscription

# Register your models here.

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Newsletter)
admin.site.register(AboutPage)
admin.site.register(CoreValue)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(NewsletterSubscription)