import logging
from rest_framework import serializers
from doors.models import Door, FeatureCategory, Feature, FilterValue, Filter, Image

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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Door
        fields = ['id', 'image', 'title', 'price', 'article']

    def get_image(self, obj):
        return ImageSerializer(obj.images.all(),  context={'request': self.context.get('request')}, many=True).data




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

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['id', 'date_added', 'url', 'mimetype']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ListViewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'price',
            'images',
            'description',
            'delivery',
            'payment',
            'safeguards',
        ]

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(),  context={'request': self.context.get('request')}, many=True).data


class DetailViewSerializer(serializers.ModelSerializer):
    feature_categories = serializers.SerializerMethodField()
    similar_doors = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'price',

            'images',

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
        return MainPageCatalogSerializer(similar_doors_sorted, context={'request': self.context.get('request')}, many=True).data

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(),  context={'request': self.context.get('request')}, many=True).data


class FilterSerializer(serializers.ModelSerializer):
    """
    Serializer for the filters for filters/ API
    """
    values = serializers.SerializerMethodField()

    class Meta:
        model = Filter
        fields = ['name', 'slug', 'values']

    def get_values(self, obj):
        return FilterValueSerializer(obj.filter_values.all(), many=True).data


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

        queryset = FilterValue.objects.filter(filter=obj, slug__in=Feature.objects.filter(
            feature_category__door__in=doors).values_list('value_slug', flat=True)).only('name', 'slug')

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
