#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_serializers
------------

Tests for `parkrundata` serializers module.
"""

from decimal import Decimal

from django.test import TestCase

from parkrundata.models import Country, Event
from parkrundata.serializers import CountrySerializer, EventSerializer


class TestCountrySerializer(TestCase):

    def setUp(self):
        self.country_data = {
            "name": "UK",
            "url": "www.parkrun.org.uk"
        }

        self.serializer_data = {
            "name": "Germany",
            "url": "www.parkrun.com.de"
        }

        self.country = Country.objects.create(**self.country_data)
        self.serializer = CountrySerializer(instance=self.country)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ["name", "url"])

    def test_name_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["name"], self.country_data["name"])

    def test_url_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["url"], self.country_data["url"])

    def test_invalid_url(self):
        self.serializer_data["url"] = "www.parkrun"

        serializer = CountrySerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ["url"])

    def tearDown(self):
        pass


class TestEvent(TestCase):

    def setUp(self):
        self.uk = Country(name="UK", url="www.parkrun.org.uk")
        self.uk.save()

        self.germany = Country(name="Germany", url="www.parkrun.com.de")
        self.germany.save()

        self.event_data = {
            "country": self.uk,
            "name": "Somecity Somepark",
            "slug": "somecitysomepark",
            "latitude": "1.234567",
            "longitude": "3.141592"
        }

        self.serializer_data = {
            "country": self.uk.id,
            "name": "Anothercity Anotherpark",
            "slug": "anothercityanotherpark",
            "latitude": "0.101010",
            "longitude": "1.010101"
        }

        self.event = Event.objects.create(**self.event_data)
        self.serializer = EventSerializer(instance=self.event)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(
            data.keys(), ["country", "name", "slug", "latitude", "longitude"]
        )

    def test_country_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["country"], self.event_data["country"].id)

    def test_name_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["name"], self.event_data["name"])

    def test_slug_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["slug"], self.event_data["slug"])

    def test_latitude_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["latitude"], self.event_data["latitude"])

    def test_longitude_field_content(self):
        data = self.serializer.data

        self.assertEqual(data["longitude"], self.event_data["longitude"])

    def test_assign_country_by_id(self):
        self.serializer_data["country"] = self.germany.id
        serializer = EventSerializer(data=self.serializer_data)

        self.assertTrue(serializer.is_valid())

        new_event = serializer.save()
        new_event.refresh_from_db()

        self.assertEqual(new_event.country, self.germany)

    def test_large_long_and_lat(self):
        self.serializer_data["latitude"] = "90.001"
        self.serializer_data["longitude"] = "180.001"
        serializer = EventSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(
                serializer.errors.keys(), ["latitude", "longitude"])

    def test_small_long_and_lat(self):
        self.serializer_data["latitude"] = "-90.001"
        self.serializer_data["longitude"] = "-180.001"
        serializer = EventSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(
                serializer.errors.keys(), ["latitude", "longitude"])

    def test_acceptable_long_and_lats(self):
        values = [
            ("90", "180"),
            ("89.999999", "179.999999"),
            ("-90", "-180"),
            ("-89.999999", "-179.999999")
        ]

        for latitude, longitude in values:
            self.serializer_data["latitude"] = latitude
            self.serializer_data["longitude"] = longitude
            serializer = EventSerializer(data=self.serializer_data)

            self.assertTrue(serializer.is_valid())

            new_event = serializer.save()
            new_event.refresh_from_db()

            self.assertEqual(new_event.latitude, Decimal(latitude))
            self.assertEqual(new_event.longitude, Decimal(longitude))

    def test_long_and_lat_precision(self):
        self.serializer_data["longitude"] = "3.14"
        self.serializer_data["latitude"] = "-3.14"

        serializer = EventSerializer(data=self.serializer_data)

        self.assertTrue(serializer.is_valid())

        new_event = serializer.save()
        new_event.refresh_from_db()

        data = EventSerializer(instance=new_event).data

        self.assertEqual(data["longitude"], "3.140000")
        self.assertEqual(data["latitude"], "-3.140000")

    def tearDown(self):
        pass
