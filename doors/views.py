from doors.models import Door, Filter
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer, FilterSerializer, \
    DoorFiltersSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import status

from doors.services import DoorFiltersService, DetailViewDoorsService


class MainPageDoorsAPIView(generics.ListAPIView):
    """
    API View for the main page that provides doors list.
    """
    queryset = Door.objects.all()
    serializer_class = MainPageCatalogSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['click_counter']

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListViewDoorsAPIView(generics.ListAPIView):
    """
    API View for the list page that provides doors list.
    """
    queryset = Door.objects.all()
    serializer_class = ListViewSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DetailViewDoorsAPIView(generics.RetrieveAPIView):
    """
    API View for the detail page that provides doors detail.
    """
    queryset = Door.objects.all()
    serializer_class = DetailViewSerializer

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        """
        Return detail view page for doors and count clicks
        """
        instance = self.get_object()
        DetailViewDoorsService.count_clicks(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ListFiltersAPIView(generics.ListAPIView):
    """
    API View for the list page that provides filters list.
    """
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DoorsFiltersAPIView(generics.ListAPIView):
    """
    API View for the list page that provides doors and filters list.
    """

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        doors, prices = DoorFiltersService.get_doors_and_prices(request)
        filters = DoorFiltersService.get_filter_queryset(request)

        door_serializer = DoorFiltersSerializer(doors, many=True)

        filter_serializer_data = DoorFiltersService.get_filter_serializer(filters, doors, prices)

        return Response({
            'doors': door_serializer.data,
            'filters': filter_serializer_data
        }, status=status.HTTP_200_OK)
