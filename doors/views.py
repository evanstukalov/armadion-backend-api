import logging

from django.core.exceptions import FieldError

from doors.models import Door, Filter
from doors.serializer import MainPageCatalogSerializer, DetailViewSerializer, ListViewSerializer, FilterSerializer
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
        Get queryset for filters.
        """
        queryset = Filter.objects.all()

        return queryset

    def get_queryset(self):
        """
        Get queryset for doors.
        """
        queryset = Door.objects.all()

        for key, value in self.request.query_params.items():
            if key is not None:
                logger.warning(f"{key:} {value}")
                match key:

                    case 'min_price':
                        queryset = queryset.filter(price__gte=value)

                    case 'max_price':
                        queryset = queryset.filter(price__lte=value)

                    case _:
                        logger.warning('else statement')
                        queryset = queryset.filter(**{key: value})

                logger.warning(f"{key:} {value}")

        return queryset

    def get(self, request, *args, **kwargs):
        filters = self.get_filter_queryset()
        doors = self.get_queryset()
        # TODO: add pagination for doors

        filter_serializer = FilterSerializer(filters, many=True)
        door_serializer = DetailViewSerializer(doors, many=True)

        return Response({
            'doors': door_serializer.data,
            'filters': filter_serializer.data,
        })
