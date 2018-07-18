# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Country, Event


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "url"]


class EventSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=8, decimal_places=6,
                                        min_value=-90, max_value=90)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6,
                                         min_value=-180, max_value=180)

    class Meta:
        model = Event
        fields = [
            "id", "country", "name", "slug",
            "latitude", "longitude"
        ]
