import json

from django.http import HttpResponse
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views import TokenView
from rest_framework import generics

from testoath2.models import CustomUser
from testoath2.serializers import Userserializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [TokenHasReadWriteScope]
    queryset = CustomUser.objects.all()
    serializer_class = Userserializer


# class UserRegister(OAuthLibMixin, APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     server_class = oauth2_settings.OAUTH2_SERVER_CLASS
#     validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
#     oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS
#     def get_available_scopes(self, application=None, request=None, *args, **kwargs):
#         return ['read','write']
#
#     def post(self, request):
#         if request.auth is None:
#             data = request.data
#             data = data.dict()
#             serializer = serializers.Userserializer(data=data)
#             if serializer.is_valid():
#                 try:
#                     with transaction.atomic():
#                         user = serializer.save()
#
#                         url, headers, body, token_status = self.create_token_response(request)
#                         if token_status != 200:
#                             raise Exception(json.loads(body).get("error_description", ""))
#
#                         return Response(json.loads(body), status=token_status)
#                 except Exception as e:
#                     return Response(data={"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_403_FORBIDDEN)
class CustomGenerateToken  (TokenView):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):

        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response