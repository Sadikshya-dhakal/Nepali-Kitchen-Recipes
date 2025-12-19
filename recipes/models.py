from django.db import models


# Create your models here.

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
    
    # For gradient colors in category cards (Tailwind CSS classes)
    gradient_from = models.CharField(max_length=50, default="blue-500", help_text="Tailwind color")
    gradient_to = models.CharField(max_length=50, default="purple-500", help_text="Tailwind color")
    
    # Display order
    order = models.IntegerField(default=0, help_text="Display order on home page")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "category"
        verbose_name_plural = "categories"



class Recipe(TimeStampModel):
    """
    Main Recipe Model
    Displays in "Trending Now" section on home page
    """
    
    # Status choices
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    
    # Difficulty choices
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Brief description for recipe cards")
    content = models.TextField(blank=True, help_text="Detailed recipe content")
    featured_image = models.ImageField(upload_to="recipes/%Y/%m/%d", blank=False)
    
    # Author
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="recipes")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    
    # Engagement metrics
    views_count = models.PositiveBigIntegerField(default=0)
    likes_count = models.PositiveBigIntegerField(default=0)
    
    # Recipe-specific fields
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=4, help_text="Number of servings")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    
    # Featured flags
    is_trending = models.BooleanField(default=False, help_text="Show in trending section on home page")
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-published_at"]
    
    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time


class Newsletter(TimeStampModel):
    """Newsletter subscriptions from home page"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-created_at"]

