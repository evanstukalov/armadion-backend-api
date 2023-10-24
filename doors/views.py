
from doors.models import Door
from doors.serializer import MainPageCatalogSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters


class DoorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides default `list` and `retrieve` actions.
    """
    queryset = Door.objects.all()
    serializer_class = MainPageCatalogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['click_counter']

