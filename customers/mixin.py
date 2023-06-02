import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse,redirect
from django.views import View


class Jwt_Login_Mixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if token:=request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                if user_id:
                    user = get_user_model().objects.get(pk=user_id)
                    # print("-----------------")
                    # print(user)
                    # print("----------------")
                    if str(user.pk) == str(kwargs.get('pk')):
                        request.user = user  # Set authenticated user on the request
                        # print(super().dispatch(request, *args, **kwargs))
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        url = reverse('api:login')
                        response = HttpResponseRedirect(url)
                        # print("----------",response)
                        return response
                else:
                    return HttpResponse('User not found.', status=401)
            except jwt.ExpiredSignatureError:
                return HttpResponse('JWT token has expired.', status=401)
            except jwt.InvalidTokenError:
                return HttpResponse('Invalid JWT token.', status=401)
        else:
            url = reverse('api:login')
            response = HttpResponseRedirect(url)
            return response