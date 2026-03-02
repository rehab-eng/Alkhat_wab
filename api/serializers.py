from rest_framework import serializers

from .models import Project, Stat, Truck


class TruckSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = ('id', 'title', 'description', 'image', 'image_url')

    def get_image_url(self, obj):
        if not obj.image:
            return None
        url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url


class ProjectSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'date', 'image', 'image_url')

    def get_image_url(self, obj):
        if not obj.image:
            return None
        url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('id', 'key', 'value', 'suffix', 'order', 'updated_at')
        read_only_fields = ('updated_at',)
