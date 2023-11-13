from django.db import connection
import logging
from decimal import Decimal

from django.db.models import Max, Min

from doors.models import Door, Filter, Feature
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer, FilterSerializer, \
    DoorFiltersSerializer, DynamicFilterSerializer
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


logger = logging.getLogger(__name__)

class DoorsFiltersAPIView(generics.ListAPIView):
    """
    API View for the list page that provides doors and filters list.
    """

    def get_filter_queryset(self):
        """
        Get queryset for filters
        """
        queryset = Filter.objects.all()
        logger.debug(f'filter: {queryset}')
        doors = self.get_queryset().prefetch_related('feature_categories__features')
        logger.debug(f'doors: {doors}')

        value_slugs = Feature.objects.filter(feature_category__door__in=doors).values_list('value_slug', flat=True)
        logger.debug(f'value_slugs: {value_slugs}')

        queryset = queryset.filter(filter_values__slug__in=value_slugs).distinct()

        logger.debug(f'filter_queryset: {queryset}')

        return queryset

    def get_queryset(self):
        """
        Get queryset for doors.
        """
        filters = {filter.slug: filter.type for filter in Filter.objects.all()}
        queryset = Door.objects.all().prefetch_related('feature_categories__features')

        for key, value in self.request.query_params.items():
            if key is not None:
                values = value.split(',')
                logger.debug(f'key, value: {key, value}')
                filter_type = filters.get(key)
                logger.debug(f'type: {filter_type}')
                if filter_type == 'category_filter':
                    queryset = queryset.filter(
                        feature_categories__features__value_slug__in=values)
                elif filter_type == 'price_filter':
                    logger.debug(f'price filter: {value}')
                    min_price, max_price = map(Decimal, value.split(','))
                    queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        prices = queryset.aggregate(Max('price'), Min('price'))

        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        doors = queryset[offset:offset + limit]

        filters = self.get_filter_queryset()

        logger.debug(f'filters: {filters}')

        context = {'doors': doors}

        door_serializer = DoorFiltersSerializer(doors, many=True)

        filter_serializer = DynamicFilterSerializer(filters, many=True, context=context)

        return Response({
            'doors': door_serializer.data,
            'filters': (filter_serializer.data + [
                {
                    'name': 'Цена',
                    'slug': 'price_filter',
                    'values': [
                        {
                            'name': 'Минимальная цена',
                            'slug': 'min_price',
                            'value': prices['price__min']
                        },
                        {
                            'name': 'Максимальная цена',
                            'slug': 'max_price',
                            'value': prices['price__max']
                        }
                    ]
                }
            ]
        )})
