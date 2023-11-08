import logging

from django.core.exceptions import FieldError
from django.db.models import Prefetch, F

from doors.models import Door, Filter, Feature, FilterValue
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer, FilterSerializer, \
    DoorFiltersSerializer, FilterValueSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        is_allowed_counter = self.request.GET.get('is_allowed_counter')
        if is_allowed_counter and is_allowed_counter.lower() == 'true':
            instance.click_counter += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListFiltersAPIView(generics.ListAPIView):
    """
    API View for the list page that provides filters list.
    """
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer


class DoorFiltersView(generics.ListAPIView):
    """
    API View for the list page that provides doors and filters list.
    """


    def get_filter_queryset(self):
        queryset = Filter.objects.all()
        logger.warning(f'filter: {queryset}')
        doors = self.get_queryset()
        logger.warning(f'doors: {doors}')
        # Create a list of slugs that exist in the doors queryset
        slugs_in_doors = doors.values_list('feature_categories__features__value_slug', flat=True)

        logger.warning(f'slugs_in_doors: {slugs_in_doors}')
        # Exclude the Filter objects from the queryset
        queryset = queryset.filter(filter_values__slug__in=slugs_in_doors).distinct()

        logger.warning(f'filter_queryset: {queryset}')

        return queryset

    def get_queryset(self):
        """
        Get queryset for doors.
        """
        queryset = Door.objects.all()

        for key, value in self.request.query_params.items():
            if key is not None:
                match key:
                    case 'min_price':
                        queryset = queryset.filter(price__gte=value)

                    case 'max_price':
                        queryset = queryset.filter(price__lte=value)

                    case _:
                        queryset = queryset.prefetch_related('feature_categories__features').filter(feature_categories__features__value_slug=value)

        return queryset


    def get(self, request, *args, **kwargs):

        doors = self.get_queryset()
        filters = self.get_filter_queryset()

        context = {'doors': doors}

        door_serializer = DoorFiltersSerializer(doors, many=True)
        filter_serializer = FilterSerializer(filters, many=True, context=context)


        return Response({
            'doors': door_serializer.data,
            'filters': filter_serializer.data
        })

