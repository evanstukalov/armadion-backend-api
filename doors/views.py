from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from doors.models import Door
from doors.serializer import DoorCarouselSerializer
from rest_framework.response import Response


class DoorListAPIView(generics.ListAPIView):
    """
    API view for listing doors.
    """
    serializer_class = DoorCarouselSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['popular']
    queryset = Door.objects.all()
    pagination_class = PageNumberPagination
    page_size = 10


