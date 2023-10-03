from rest_framework import serializers

from .models import Image, ExpiringLink


class ImageListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'images'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return obj.get_links(request)


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image'
        ]


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            'link'
        ]


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            'image',
            'time_to_expired'
        ]
