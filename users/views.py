from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .utils import getTokensForUser

from .serializers import SignInSerializer, SignUpSerializer


@extend_schema(
    request=SignUpSerializer,
    responses={201: {"description": "User registered successfully"}},
    tags=["Authentication"],
)
@api_view(["POST"])
@permission_classes(
    [AllowAny]
)  # Allow any user (authenticated or not) to access this view
def sign_up(request):
    """API view for user sign-up."""
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success": True, "message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SignInSerializer,
    responses={200: {"description": "User signed in successfully"}},
    tags=["Authentication"],
)
@api_view(["POST"])
@permission_classes(
    [AllowAny]
)  # Allow any user (authenticated or not) to access this view
def sign_in(request):
    """API view for user sign-in."""

    serializer = SignInSerializer(
        data={
            "username": request.data.get("username"),
            "email": request.data.get("username"),
            "password": request.data.get("password"),
        }
    )
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        tokens = getTokensForUser(user)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(
            {
                "success": True,
                "message": "User signed in successfully",
                "user_details": user_data,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "access_expires_at": tokens["access_expires_at"],
                "access_expires_in": tokens["access_expires_in"],
                "refresh_expires_at": tokens["refresh_expires_at"],
                "refresh_expires_in": tokens["refresh_expires_in"],
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {"success": False, "message": "Invalid credentials"},
        status=status.HTTP_400_BAD_REQUEST,
    )
