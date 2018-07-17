#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` models module.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from parkrundata import models


class TestCountry(TestCase):

    def setUp(self):
        pass

    def test_create_and_retrieve_country(self):
        country = models.Country(name="UK", url="www.parkrun.org.uk")
        country.save()

        c = models.Country.objects.get()
        self.assertEqual(c.name, "UK")
        self.assertEqual(c.url, "www.parkrun.org.uk")

    def test_cannot_create_duplicate_country_name(self):
        country = models.Country(name="UK", url="http://www.parkrun.org.uk")
        country.save()

        with self.assertRaises(IntegrityError):
            models.Country.objects.create(name="UK",
                                          url="http://www.parkrun.org")

    def test_can_create_duplicate_country_url(self):
        # Note that parkrun.org use the same URL for a number of countries
        country1 = models.Country(
            name="UK", url="http://www.parkrun.org.uk")
        country1.save()
        country2 = models.Country(
            name="United Kingdom", url="http://www.parkrun.org.uk")
        country2.save()

        country1.refresh_from_db()
        country2.refresh_from_db()
        self.assertNotEqual(country1.id, country2.id)

    def tearDown(self):
        pass


class TestEvent(TestCase):

    def setUp(self):
        self.country = models.Country(name="UK", url="www.parkrun.org.uk")
        self.country.save()

    def test_create_and_retrieve_event(self):
        event = models.Event(
            country=self.country,
            name="Atownsomewhere Juniors",
            slug="atownsomewherejuniors",
            is_junior=True,
            is_restricted=True,
            is_discontinued=True,
            latitude=0,
            longitude=0,
        )
        event.save()

        e = models.Event.objects.get()
        self.assertEqual(e.country.name, "UK")
        self.assertEqual(e.name, "Atownsomewhere Juniors")
        self.assertEqual(e.slug, "atownsomewherejuniors")
        self.assertTrue(e.is_junior)
        self.assertTrue(e.is_restricted)
        self.assertTrue(e.is_discontinued)
        self.assertEqual(e.latitude, 0)
        self.assertEqual(e.longitude, 0)

    def test_boolean_fields_default_to_false(self):
        event = models.Event(
            country=self.country,
            name="Atownsomewhere",
            slug="atownsomewhere",
            latitude=0,
            longitude=0,
        )
        event.save()

        e = models.Event.objects.get()
        self.assertEqual(e.country.name, "UK")
        self.assertEqual(e.name, "Atownsomewhere")
        self.assertEqual(e.slug, "atownsomewhere")
        self.assertFalse(e.is_junior)
        self.assertFalse(e.is_restricted)
        self.assertFalse(e.is_discontinued)
        self.assertEqual(e.latitude, 0)
        self.assertEqual(e.longitude, 0)

    def test_invalid_coordinates(self):
        # Here we check that we can only save objects that have:
        # a) latitude between -99.999999 and 99.999999
        # b) longitude between -999.999999 and 999.999999
        # c) longitude and latitude with precision no greater than 6 decimals
        # More specific validation goes elsewhere (eg form/serializer)

        coords = [
            ("-100", "0"),
            ("-0.0000001", "0"),
            ("0.0000001", "0"),
            ("100", "0"),
            ("0", "-1000"),
            ("0", "-0.0000001"),
            ("0", "0.0000001"),
            ("0", "1000")
        ]

        for latitude, longitude in coords:
            event = models.Event(
                country=self.country,
                name="Atownsomewhere",
                slug="atownsomewhere",
                latitude=latitude,
                longitude=longitude,
            )
            with self.assertRaises(Exception):
                event.save()

    def test_valid_coodinates(self):
        coords = [
            ("-99.999999", "0"),
            ("-0.000001", "0"),
            ("0.000001", "0"),
            ("99.999999", "0"),
            ("0", "-999.999999"),
            ("0", "-0.000001"),
            ("0", "0.000001"),
            ("0", "999.999999")
        ]
        event = models.Event(
            country=self.country,
            name="Atownsomewhere",
            slug="atownsomewhere",
            latitude="0",
            longitude="0",
        )

        for latitude, longitude in coords:
            event.latitude = latitude
            event.longitude = longitude
            event.save()

            event.refresh_from_db()
            self.assertEqual(event.latitude, Decimal(latitude))
            self.assertEqual(event.longitude, Decimal(longitude))

    def test_cannot_create_duplicate_event_name_within_country(self):
        event1 = models.Event(
            country=self.country,
            name="Park",
            slug="park",
            latitude="0.1",
            longitude="0.1",
        )
        event1.save()

        event2 = models.Event(
            country=self.country,
            name="Park",
            slug="park2",
            latitude="0",
            longitude="0",
        )
        with self.assertRaises(IntegrityError):
            event2.save()

    def test_cannot_create_duplicate_event_slug_within_country(self):
        event1 = models.Event(
            country=self.country,
            name="Park",
            slug="park",
            latitude="0.1",
            longitude="0.1",
        )
        event1.save()

        event2 = models.Event(
            country=self.country,
            name="Park park",
            slug="park",
            latitude="0",
            longitude="0",
        )
        with self.assertRaises(IntegrityError):
            event2.save()

    def test_can_create_duplicate_event_name_for_different_country(self):
        event1 = models.Event(
            country=self.country,
            name="Park",
            slug="park",
            latitude="0.1",
            longitude="0.1",
        )
        event1.save()
        event1.refresh_from_db()

        country2 = models.Country.objects.create(
            name="Ireland", url="http://www.pakrun.ie")
        event2 = models.Event(
            country=country2,
            name="Park",
            slug="park",
            latitude="0",
            longitude="0",
        )
        event2.save()
        event2.refresh_from_db()

        self.assertNotEqual(event1.id, event2.id)

    def tearDown(self):
        pass
