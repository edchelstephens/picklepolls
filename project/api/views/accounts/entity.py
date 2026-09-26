from django.db.models import Q

from accounts.serializers import EntitySerializer
from accounts.models import Entity

from utils.view import LoginRequiredRestAPIView, RestAPIView
from utils.exceptions import HumanReadableError


class PublicEntitiesAPIView(RestAPIView):
    """Public entities api view."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""
        try:
            queryset = Entity.objects.all()
            serializer = EntitySerializer(queryset, many=True)
            data = serializer.data
            response = {"data": data, "count": len(data)}
            return self.success_response(response)
        except HumanReadableError as exc:
            return self.error_response(exc)
        except Exception as exc:
            return self.server_error_response(exc)


class EntitiesAPIView(LoginRequiredRestAPIView):
    """Entities api view."""

    def get(self, request, *args, **kwargs):
        """Handle get request."""
        try:
            user = self.get_user_instance(request)
            filters = Q(owner=user) | Q(admins=user)
            queryset = Entity.objects.filter(filters)
            serializer = EntitySerializer(instance=queryset, many=True)

            data = serializer.data
            response = {"data": data, "count": len(data)}
            return self.success_response(response)

        except HumanReadableError as exc:
            return self.error_response(exception=exc)
        except Exception as exc:
            return self.server_error_response(exception=exc)
