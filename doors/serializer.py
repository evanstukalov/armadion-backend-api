from rest_framework import serializers
from doors.models import Door, Characteristic, CategoryCharacteristic


class MainPageCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for the main page catalog
    """

    class Meta:
        model = Door
        fields = ['image_one', 'title', 'price', 'article']


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['id', 'name', 'value']


class CategoryCharacteristicSerializer(serializers.ModelSerializer):
    characteristics = CharacteristicSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryCharacteristic
        fields = ['id', 'name', 'characteristics']


class ListViewSerializer(serializers.ModelSerializer):
    category_characteristics = CategoryCharacteristicSerializer(many=True, read_only=True)

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

            'category_characteristics'
        ]


class DetailViewSerializer(serializers.ModelSerializer):
    category_characteristics = CategoryCharacteristicSerializer(many=True, read_only=True)

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

            'category_characteristics'
        ]
