from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


from utils.view import RestAPIView
from utils.exceptions import HumanReadableError


from rest_framework.authtoken.views import ObtainAuthToken


class TokenAPIView(ObtainAuthToken, RestAPIView):
    """Obtain Auth token APIView."""

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Handle post request."""
        try:
            data = request.data

            serializer = AuthTokenSerializer(data)

            if serializer.is_valid():
                user = serializer.validated_data["user"]
                token, is_created = Token.objects.get_or_create(user=user)
                response_data = {
                    "user_id": user.pk,
                    "token": token.key,
                    "email": user.email,
                    "username": user.username,
                }

                return self.success_response(response_data)
            else:
                self.raise_error(errors=serializer.errors)
        except HumanReadableError as exc:
            return self.error_response(exception=exc)
        except Exception as exc:
            return self.server_error_response(exception=exc)
