
from doors.models import Door
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import generics

class MainPageDoorsAPIView(generics.ListAPIView):
    """
    API View for the main page that provides doors list.
    """
    queryset = Door.objects.all()
    serializer_class = MainPageCatalogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['click_counter']


class DetailViewDoorsAPIView(generics.RetrieveAPIView):
    """
    API View for the detail page that provides doors detail.
    """
    queryset = Door.objects.all()
    serializer_class = DetailViewSerializer



