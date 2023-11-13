import logging

from django.db.models import Max, Min
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

class FilterSerializer(serializers.ModelSerializer):
    """
    Serializer for the filters for filters/ API
    """
    values = serializers.SerializerMethodField()

    class Meta:
        model = Filter
        fields = ['name', 'slug', 'values']


    def get_values(self, obj):
        queryset = FilterValue.objects.filter(filter=obj)
        return FilterValueSerializer(queryset, many=True).data

class FilterValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterValue
        fields = ['name', 'slug']


class DynamicFilterSerializer(serializers.ModelSerializer):
    """
    Serializer for the dynamic filters for doors/filter API
    """
    values = serializers.SerializerMethodField()

    class Meta:
        model = Filter
        fields = ['name', 'slug', 'values']

    def get_values(self, obj):
        doors = self.context.get("doors").prefetch_related('feature_categories__features')

        queryset = FilterValue.objects.filter(filter=obj, slug__in=Feature.objects.filter(feature_category__door__in=doors).values_list('value_slug', flat=True)).only('name', 'slug')

        return FilterValueSerializer(queryset, many=True).data


class DoorFiltersSerializer(serializers.ModelSerializer):
    """
    Serializer for the doors for doors/filter API
    """
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
        """
        Returns the feature categories associated with the given object.
        """
        return FeatureCategorySerializer(obj.feature_categories.all(), many=True).data
