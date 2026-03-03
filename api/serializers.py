from rest_framework import serializers

from .models import Project, SiteSetting, Stat, Statistic, Truck, Vehicle


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


class VehicleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ('id', 'title', 'description', 'image', 'image_url', 'updated_at')
        read_only_fields = ('updated_at',)

    def get_image_url(self, obj):
        if not obj.image:
            return None
        url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = (
            'id',
            'key',
            'label_en',
            'label_ar',
            'caption_en',
            'caption_ar',
            'value',
            'suffix',
            'order',
            'updated_at',
        )
        read_only_fields = ('updated_at',)


class SiteSettingSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSetting
        fields = (
            'id',
            'site_name_en',
            'site_name_ar',
            'hero_title_en',
            'hero_title_ar',
            'hero_desc_en',
            'hero_desc_ar',
            'contact_phone',
            'contact_email',
            'address_en',
            'address_ar',
            'logo',
            'logo_url',
            'hero_image',
            'hero_image_url',
            'refresh_token',
            'updated_at',
        )
        read_only_fields = ('refresh_token', 'updated_at')

    def get_logo_url(self, obj):
        if not obj.logo:
            return None
        url = obj.logo.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url

    def get_hero_image_url(self, obj):
        if not obj.hero_image:
            return None
        url = obj.hero_image.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url
