from rest_framework import serializers
from doors.models import Door, FeatureCategory, Feature


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
        fields = ['image_one', 'title', 'price', 'article']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'value']


class FeatureCategorySerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = FeatureCategory
        fields = ['id', 'name', 'features']

    def get_features(self, obj):
        return FeatureSerializer(Feature.objects.filter(pk=obj.pk), many=True).data


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
        door = Door.objects.get(pk=obj.pk)
        similar_doors = Door.objects.all().exclude(pk=obj.pk)
        similar_doors_sorted = sorted(similar_doors, key=lambda p: is_similar(door, p), reverse=True)[:3]
        return MainPageCatalogSerializer(similar_doors_sorted, many=True).data
