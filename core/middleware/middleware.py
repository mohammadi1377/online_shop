import jwt
from django.conf import settings
from django.contrib.auth import get_user_model


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self.get_user(request)

        if user:
            request.user = user
        response = self.get_response(request)

        return response

    def get_user(self, request):
        token = request.COOKIES.get('jwt')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            if user_id:
                return get_user_model().objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            pass