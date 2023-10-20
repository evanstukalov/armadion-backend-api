from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from doors.models import Door
from doors.serializer import MainPageCatalogSerializer
from rest_framework.pagination import LimitOffsetPagination


class DoorListAPIView(generics.ListAPIView):
    """
    API view for the main page catalog
    """
    serializer_class = MainPageCatalogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['popular']
    queryset = Door.objects.all()

    pagination_class = LimitOffsetPagination


