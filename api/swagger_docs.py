from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class OAuthTokenDocView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Get OAuth2 Client Token",
        description="Generate OAuth2 token using client credentials. Actual endpoint is /o/token/",
        request={
            "application/x-www-form-urlencoded": {
                "type": "object",
                "properties": {
                    "grant_type": {"type": "string", "example": "client_credentials"},
                    "client_id": {"type": "string"},
                    "client_secret": {"type": "string"},
                },
                "required": ["grant_type", "client_id", "client_secret"],
            }
        },
        responses={200: dict},
    )
    def post(self, request):
        return Response(
            {
                "access_token": "sample_access_token",  # nosec B105
                "token_type": "Bearer",  # nosec B105
                "expires_in": 3600,
            }
        )
