#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` models module.
"""

from decimal import Decimal

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

    def tearDown(self):
        pass


class TestEvent(TestCase):

    def setUp(self):
        self.country = models.Country(name="UK", url="www.parkrun.org.uk")
        self.country.save()

    def test_create_and_retrieve_event(self):
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

        for latitude, longitude in coords:
            event = models.Event(
                country=self.country,
                name="Atownsomewhere",
                slug="atownsomewhere",
                latitude=latitude,
                longitude=longitude,
            )
            event.save()
            event.refresh_from_db()
            self.assertEqual(event.latitude, Decimal(latitude))
            self.assertEqual(event.longitude, Decimal(longitude))

    def tearDown(self):
        pass
