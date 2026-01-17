from django.db import models
from tinymce.models import HTMLField


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True, help_text="Emoji")
    image = models.ImageField(upload_to="category_images/%Y/%m/%d", null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    recipe_count = models.IntegerField(default=0, help_text="Number of recipes in this category")
    gradient_from = models.CharField(max_length=50, default="blue-500", help_text="Tailwind color")
    gradient_to = models.CharField(max_length=50, default="purple-500", help_text="Tailwind color")
    order = models.IntegerField(default=0, help_text="Display order on home page")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "category"
        verbose_name_plural = "categories"


class Recipe(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = HTMLField()
    featured_image = models.ImageField(upload_to="recipes/%Y/%m/%d", blank=False)
    
    # Author and status
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="recipes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    
    # Metrics
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    
    # Recipe details
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    
    # Recipe content
    ingredients = models.TextField()
    instructions = models.TextField()
    chef_tips = models.TextField(blank=True, null=True, help_text="One tip per line")
    

    
    # Flags
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Relationship
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-published_at"]
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    @property
    def ingredients_list(self):
        if self.ingredients:
            return [i.strip() for i in self.ingredients.split('\n') if i.strip()]
        return []
    
    @property
    def instructions_list(self):
        if self.instructions:
            return [i.strip() for i in self.instructions.split('\n') if i.strip()]
        return []
    
    @property
    def tips_list(self):
        if self.chef_tips:
            return [t.strip() for t in self.chef_tips.split('\n') if t.strip()]
        return []


class Review(TimeStampModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.recipe.title}"
    
    class Meta:
        ordering = ["-created_at"]


class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-created_at"]

class AboutPage(TimeStampModel):
    mission_description = models.TextField()
    story_description = models.TextField()
    
    def __str__(self):
        return "About Page"


class CoreValue(TimeStampModel):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class OurTeam(TimeStampModel):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team_images/%Y/%m/%d")
    description = models.TextField()
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
class Contact(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_at"]

class NewsletterSubscription(TimeStampModel):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email