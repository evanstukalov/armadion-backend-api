import logging
from typing import Any

from django.db.models import Max, Min, QuerySet
from decimal import Decimal

from doors.models import Feature, Door, FeatureCategory
from doors.serializers import FeatureCategorySerializer

logger = logging.getLogger(__name__)


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
    def filter_doors_queryset(request, queryset: QuerySet) -> QuerySet:
        """
        Method to filter doors queryset.
        """

        for key, value in request.query_params.items():
            if key is not None:
                try:
                    values = value.split(',')

                    if 'price' in key:
                        values = value.split(',')
                        min_price, max_price = map(Decimal, values)
                        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

                    elif 'limit' in key or 'offset' in key:
                        continue

                    else:
                        queryset = queryset.filter(
                            features__value_slug__in=values)

                except Exception as e:
                    logger.error(e)
                    continue

        return queryset

    @staticmethod
    def get_features_queryset(request):
        """
        Get queryset for filters
        """
        all_features = Feature.objects.all()
        doors = DoorFiltersService.get_queryset(request).prefetch_related('features')

        return all_features.filter(door__in=doors).distinct()

    @staticmethod
    def get_feature_category_queryset(request, features) -> QuerySet:
        """
        Get queryset for filters
        """
        queryset = FeatureCategory.objects.filter(features__in=features).distinct()

        return queryset

    @staticmethod
    def get_queryset(request) -> QuerySet:
        """
        Get queryset for doors.
        """
        all_doors = Door.objects.all().prefetch_related('features')

        queryset = DoorFiltersService.filter_doors_queryset(request, all_doors)

        return queryset

    @staticmethod
    def get_doors(request) -> QuerySet:
        queryset = DoorFiltersService.get_queryset(request)
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        doors = queryset[offset:offset + limit]

        return doors

    @staticmethod
    def get_prices(queryset: QuerySet) -> dict:
        return queryset.aggregate(Max('price'), Min('price'))

    @staticmethod
    def get_filter_serializer(request, prices: dict) -> Any:
        features = DoorFiltersService.get_features_queryset(request)
        feature_categories = DoorFiltersService.get_feature_category_queryset(request, features)

        return FeatureCategorySerializer(feature_categories, many=True,
                                         context={'request': request, 'features': features}).data + [
            {
                'name': 'Цена',
                'slug': 'price',
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
