import logging
from rest_framework import serializers
from doors.models import Door, FeatureCategory, Feature, Image

from loguru import logger


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
        return ImageSerializer(obj.images.all(), context={'request': self.context.get('request')}, many=True).data


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
        logger.info(self.context['features'].all())
        logger.info(obj)
        return FeatureSerializer(self.context['features'].filter(feature_category=obj), many=True).data



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
        return ImageSerializer(obj.images.all(), context={'request': self.context.get('request')}, many=True).data


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
        return FeatureCategorySerializer([feature.feature_category for feature in obj.features.all()], many=True).data

    def get_similar_doors(self, obj):
        door = Door.objects.get(id=obj.id)
        similar_doors = Door.objects.all().exclude(id=obj.id)
        similar_doors_sorted = sorted(similar_doors, key=lambda p: is_similar(door, p), reverse=True)[:3]
        return MainPageCatalogSerializer(similar_doors_sorted, context={'request': self.context.get('request')},
                                         many=True).data

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), context={'request': self.context.get('request')}, many=True).data


class DoorFiltersSerializer(serializers.ModelSerializer):
    """
    Serializer for the doors for doors/filter API
    """
    images = serializers.SerializerMethodField()
    feature_categories = serializers.SerializerMethodField()

    class Meta:
        model = Door
        fields = [
            'id',
            'title',
            'images',
            'price',
            'feature_categories',
        ]

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), context={'request': self.context.get('request')}, many=True).data

    def get_feature_categories(self, obj):
        """
        Returns the feature categories associated with the given object.
        """
        return FeatureCategorySerializer([feature.feature_category for feature in obj.features.all()],
                                         context={'features': obj.features}, many=True).data
