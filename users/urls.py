from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),  # User sign-up endpoint
    path("signin/", views.sign_in, name="signin"),  # User sign-in endpoint
]
