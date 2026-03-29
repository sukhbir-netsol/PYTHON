from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

user = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for user sign-up."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """Meta class for SignUpSerializer."""

        model = user
        fields = ("username", "email", "password")

    def create(self, validated_data):
        """Create a new user with the validated data."""
        user_instance = user.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user_instance


class SignInSerializer(serializers.Serializer):
    """Serializer for user sign-in."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate user credentials."""
        email = data.get("email")
        password = data.get("password")
        user_instance = authenticate(email=email, password=password)
        if not user_instance:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user_instance
        return data
