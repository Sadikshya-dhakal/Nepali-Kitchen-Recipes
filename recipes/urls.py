from django.urls import path
from recipes import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]