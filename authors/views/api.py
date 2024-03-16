from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from ..serializers import AuthorSerializer


class AuthorAPIv2ViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(
            username=self.request.user.username
        )

        return qs
