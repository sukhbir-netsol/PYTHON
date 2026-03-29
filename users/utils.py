"""
Reusable utilities for the users app.
"""

from datetime import datetime, timezone as utc_tz
from typing import TYPE_CHECKING

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

    User = get_user_model()


def getTokensForUser(user: "User") -> dict:
    """
    Generate access and refresh JWT tokens for an authenticated user.

    Uses rest_framework_simplejwt. Respects SIMPLE_JWT settings (lifetimes,
    signing key, etc.). When ROTATE_REFRESH_TOKENS and BLACKLIST_AFTER_ROTATION
    are enabled, refresh tokens are tracked and blacklisted on use.

    Args:
        user: Django user instance (must have pk and be saved).

    Returns:
        dict with keys:
            - access: str (Bearer token for Authorization header)
            - refresh: str (use at /api/token/refresh/ to get new access token)
            - access_expires_at: str (ISO 8601 UTC datetime when access token expires)
            - access_expires_in: int (seconds until access token expires)
            - refresh_expires_at: str (ISO 8601 UTC datetime when refresh token expires)
            - refresh_expires_in: int (seconds until refresh token expires)

    Raises:
        TypeError: If user is not a valid user instance.
    """
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    refresh_payload = refresh.payload

    now = timezone.now()
    access_exp_timestamp = access_token.payload["exp"]
    refresh_exp_timestamp = refresh_payload["exp"]

    access_expires_at = datetime.fromtimestamp(access_exp_timestamp, tz=utc_tz.utc)
    refresh_expires_at = datetime.fromtimestamp(refresh_exp_timestamp, tz=utc_tz.utc)

    access_expires_in = int(access_exp_timestamp - now.timestamp())
    refresh_expires_in = int(refresh_exp_timestamp - now.timestamp())

    return {
        "access": str(access_token),
        "refresh": str(refresh),
        "access_expires_at": access_expires_at.isoformat(),
        "access_expires_in": access_expires_in,
        "refresh_expires_at": refresh_expires_at.isoformat(),
        "refresh_expires_in": refresh_expires_in,
    }
