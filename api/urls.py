from django.urls import path
from .swagger_docs import OAuthTokenDocView

urlpatterns = [
    path("auth/oauth/token/", OAuthTokenDocView.as_view()),
]
