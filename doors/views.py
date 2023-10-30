import logging

from doors.models import Door
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def is_similar(product1, product2):
    """
    Check if two products are similar
    :param product1:
    :param product2:
    :return:
    """
    logger.warning(product1.price)
    logger.warning(product2.price)
    return product1.price == product2.price

class MainPageDoorsAPIView(generics.ListAPIView):
    """
    API View for the main page that provides doors list.
    """
    queryset = Door.objects.all()
    serializer_class = MainPageCatalogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['click_counter']

class ListViewDoorsAPIView(generics.ListAPIView):
    """
    API View for the list page that provides doors list.
    """
    queryset = Door.objects.all()
    serializer_class = ListViewSerializer


class DetailViewDoorsAPIView(generics.RetrieveAPIView):
    """
    API View for the detail page that provides doors detail.
    """
    queryset = Door.objects.all()
    serializer_class = DetailViewSerializer

class SimilarDoorsAPIView(generics.ListAPIView):
    """
    API View that provides similar products
    """
    serializer_class = MainPageCatalogSerializer

    def get_queryset(self):
        door_id = self.kwargs.get('pk')
        door = Door.objects.get(pk=door_id)
        similar_doors = Door.objects.all().exclude(pk=door_id)
        logger.warning(similar_doors)
        similar_doors_sorted = sorted(similar_doors, key=lambda p: is_similar(door, p), reverse=True)[:3]
        logger.warning(similar_doors_sorted)
        return similar_doors_sorted


