from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from accounts.serializers import EmailAuthTokenSerializer


from utils.view import RestAPIView, LoginRequiredRestAPIView
from utils.exceptions import HumanReadableError


class ObtainTokenAPIView(ObtainAuthToken, RestAPIView):
    """Obtain Auth token APIView."""

    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Handle post request."""
        try:
            data = request.data

            serializer = EmailAuthTokenSerializer(data=data)

            if serializer.is_valid():
                user = serializer.validated_data["user"]
                token, is_created = Token.objects.get_or_create(user=user)
                response_data = {
                    "id": user.pk,
                    "token": token.key,
                    "email": user.email,
                }

                return self.success_response(response_data)
            else:
                self.raise_error(errors=serializer.errors)
        except HumanReadableError as exc:  # pragma no cover
            return self.error_response(exception=exc)
        except Exception as exc:  # pragma no cover
            return self.server_error_response(exception=exc)


class DestroyTokenAPIView(LoginRequiredRestAPIView):
    """Detroy token API view."""

    def post(self, request, *args, **kwargs):
        """Handle post request."""
        try:
            user = self.get_user_instance(request)
            Token.objects.filter(user=user).delete()

            response = {"title": "Success", "message": "Logged out successfully!"}
            return self.success_response(response)
        except HumanReadableError as exc:  # pragma no cover
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)
