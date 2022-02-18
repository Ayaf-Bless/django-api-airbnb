from typing import Tuple

from users.models import User
import jwt
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings


class JWTAuth(authentication.BaseAuthentication):
    def authenticate(self, request) -> tuple[User, None] | None:
        try:
            token: str = request.META.get("HTTP_AUTHORIZATION")
            if not token:
                return None
            bearer, jwt_token = token.split(" ")
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms="HS256")
            pk = decoded.get("user_id")
            user = User.objects.get(pk=pk)
            return user, None
        except (ValueError, User.DoesNotExist):
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="token format invalid")
