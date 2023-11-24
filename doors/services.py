from typing import Any

from django.db.models import Max, Min, QuerySet
from decimal import Decimal

from doors.models import Filter, Feature, Door
from doors.serializer import DynamicFilterSerializer


class DetailViewDoorsService:
    @staticmethod
    def count_clicks(request, instance) -> None:
        """
        Service for counting clicks.
        """
        is_allowed_counter = request.GET.get('is_allowed_counter')
        if is_allowed_counter and is_allowed_counter.lower() == 'true':
            instance.click_counter += 1
            instance.save()


class DoorFiltersService:

    @staticmethod
    def filter_doors_queryset(request, queryset: QuerySet, filters: dict) -> QuerySet:
        """
        Method to filter doors queryset.
        """
        for key, value in request.query_params.items():
            print(key, value)
            if key is not None:
                values = value.split(',')
                filter_type = filters.get(key)
                print(filter_type)
                if filter_type == 'category_filter':
                    queryset = queryset.filter(
                        feature_categories__features__value_slug__in=values)
                elif filter_type == 'price_filter':
                    values = value.split(',')
                    min_price, max_price = map(Decimal, values)
                    queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

    @staticmethod
    def get_filter_queryset(request) -> QuerySet:
        """
        Get queryset for filters
        """
        queryset = Filter.objects.all()
        doors = DoorFiltersService.get_queryset(request).prefetch_related('feature_categories__features')
        value_slugs = Feature.objects.filter(feature_category__door__in=doors).values_list('value_slug', flat=True)
        queryset = queryset.filter(filter_values__slug__in=value_slugs).distinct()
        return queryset

    @staticmethod
    def get_queryset(request) -> QuerySet:
        """
        Get queryset for doors.
        """

        filters = {filter.slug: filter.type for filter in Filter.objects.all()}
        queryset = Door.objects.all().prefetch_related('feature_categories__features')

        queryset = DoorFiltersService.filter_doors_queryset(request, queryset, filters)

        return queryset

    @staticmethod
    def get_doors_and_prices(request) -> tuple[QuerySet, dict]:
        queryset = DoorFiltersService.get_queryset(request)
        prices = queryset.aggregate(Max('price'), Min('price'))
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        doors = queryset[offset:offset + limit]

        return doors, prices

    @staticmethod
    def get_filter_serializer(filters: QuerySet, doors: QuerySet, prices: dict) -> Any:
        return DynamicFilterSerializer(filters, many=True, context={'doors': doors}).data + [
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
