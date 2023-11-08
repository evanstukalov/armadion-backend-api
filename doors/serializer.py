import logging

from rest_framework import serializers

from doors.models import Door, FeatureCategory, Feature, FilterValue, Filter

logger = logging.getLogger(__name__)


def is_similar(product1: Door, product2: Door) -> bool:
    """
    Check if two products are similar
    :param product1:
    :param product2:
    :return:
    """
    return product1.price == product2.price


class MainPageCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for the main page catalog
    """

    class Meta:
        model = Door
        fields = ['id', 'image_one', 'title', 'price', 'article']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name', 'value', 'name_slug', 'value_slug']


class FeatureCategorySerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = FeatureCategory
        fields = ['name', 'slug', 'features']

    def get_features(self, obj):
        return FeatureSerializer(Feature.objects.filter(feature_category=obj), many=True).data


class ListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'price',

            'image_one',
            'image_two',
            'image_three',
            'image_four',

            'description',
            'delivery',
            'payment',
            'safeguards',
        ]


class DetailViewSerializer(serializers.ModelSerializer):
    feature_categories = serializers.SerializerMethodField()
    similar_doors = serializers.SerializerMethodField()

    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'price',

            'image_one',
            'image_two',
            'image_three',
            'image_four',

            'description',
            'delivery',
            'payment',
            'safeguards',

            'feature_categories',
            'similar_doors'
        ]

    def get_feature_categories(self, obj):
        return FeatureCategorySerializer(FeatureCategory.objects.filter(door=obj), many=True).data

    def get_similar_doors(self, obj):
        door = Door.objects.get(id=obj.id)
        similar_doors = Door.objects.all().exclude(id=obj.id)
        similar_doors_sorted = sorted(similar_doors, key=lambda p: is_similar(door, p), reverse=True)[:3]
        return MainPageCatalogSerializer(similar_doors_sorted, many=True).data


class FilterValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterValue
        fields = ['name', 'slug']


class FilterSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()

    class Meta:
        model = Filter
        fields = ['name', 'slug', 'values']

    def get_values(self, obj):
        queryset = FilterValue.objects.all()
        logger.warning('<==================')
        logger.warning(obj)
        logger.warning(f'filter_values: {queryset}')

        doors = self.context.get("doors").prefetch_related('feature_categories__features')
        logger.warning(f'doors: {doors}')

        value_slugs = Feature.objects.filter(feature_category__door__in=doors).values_list('value_slug', flat=True)
        logger.warning(f'value_slugs: {value_slugs}')

        # Exclude the Filter objects from the queryset
        queryset = queryset.filter(slug__in=value_slugs).filter(filter=obj)
        logger.warning(f'filter_values queryset: {queryset}')
        logger.warning('==================>')

        return FilterValueSerializer(queryset, many=True).data


class DoorFiltersSerializer(serializers.ModelSerializer):
    feature_categories = serializers.SerializerMethodField()

    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'price',
            'feature_categories',
        ]

    def get_feature_categories(self, obj):
        return FeatureCategorySerializer(FeatureCategory.objects.filter(door=obj), many=True).data
