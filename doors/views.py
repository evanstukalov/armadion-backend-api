import logging

from doors.models import Door, Filter, Feature
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer, FilterSerializer, \
    DoorFiltersSerializer
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
        """
        Get queryset for filters
        """
        queryset = Filter.objects.all()
        logger.warning(f'filter: {queryset}')
        doors = self.get_queryset().prefetch_related('feature_categories__features')
        logger.warning(f'doors: {doors}')

        value_slugs = Feature.objects.filter(feature_category__door__in=doors).values_list('value_slug', flat=True)
        logger.warning(f'value_slugs: {value_slugs}')

        # Exclude the Filter objects from the queryset
        queryset = queryset.filter(filter_values__slug__in=value_slugs).distinct()

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

                    case 'limit':
                        pass

                    case 'offset':
                        pass

                    case _:
                        queryset = queryset.prefetch_related('feature_categories__features').filter(
                            feature_categories__features__value_slug=value)

        return queryset

    def get(self, request, *args, **kwargs):

        limit = int(request.query_params.get('limit', 10))  # default limit to 10 if not provided
        offset = int(request.query_params.get('offset', 0))  # default offset to 0 if not provided

        doors = self.get_queryset()[offset:offset + limit]
        logger.warning(f'doors: {doors}')

        filters = self.get_filter_queryset()

        logger.warning(f'filters: {filters}')

        context = {'doors': doors}

        # doors = doors

        door_serializer = DoorFiltersSerializer(doors, many=True)

        filter_serializer = FilterSerializer(filters, many=True, context=context)

        return Response({
            'doors': door_serializer.data,
            'filters': filter_serializer.data
        })
