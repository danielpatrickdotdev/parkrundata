#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` models module.
"""

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
        self.assertEqual(e.latitude, 0)
        self.assertEqual(e.longitude, 0)

    def tearDown(self):
        pass
