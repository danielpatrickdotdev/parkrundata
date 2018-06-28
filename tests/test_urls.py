#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` urls module.
"""

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from parkrundata import models


class TestCountry(TestCase):

    def setUp(self):
        self.uk = models.Country.objects.create(
                name="UK", url="www.parkrun.org.uk")
        self.france = models.Country.objects.create(
                name="France", url="www.parkrun.fr")
        self.germany = models.Country.objects.create(
                name="Germany", url="www.parkrun.com.de")

        self.bushy_data = {
            "country": self.uk,
            "name": "Bushy",
            "slug": "bushy",
            "latitude": "51.409694",
            "longitude": "-0.334032"
        }
        self.bushy = models.Event.objects.create(**self.bushy_data)
        self.bushy_data["country"] = 1

        self.lesdougnes_data = {
            "country": self.france,
            "name": "Les Dougnes",
            "slug": "lesdougnes",
            "latitude": "45.066553",
            "longitude": "-0.429266"
        }
        self.lesdougnes = models.Event.objects.create(**self.lesdougnes_data)
        self.lesdougnes_data["country"] = 2

        self.neckarau_data = {
            "country": self.germany,
            "name": "Neckarau",
            "slug": "neckarau",
            "latitude": "49.448549",
            "longitude": "8.453786"
        }
        self.neckarau = models.Event.objects.create(**self.neckarau_data)
        self.neckarau_data["country"] = 3

        self.client = APIClient()

    def test_retrieve_event_returns_correct_object(self):
        response = self.client.get("/events/1/", format="json")
        bushy_data = self.bushy_data
        self.assertEqual(response.data, bushy_data)

    def test_retrieve_event_incorrect_url_gets_404(self):
        response = self.client.get("/events/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_event_gets_405(self):
        response = self.client.post("/events/1/", data={"name": "Bushy Park"})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_event_gets_405(self):
        response = self.client.delete("/events/1/")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_event_list(self):
        response = self.client.get("/events/")
        parkruns_data = [
            self.bushy_data, self.lesdougnes_data, self.neckarau_data]
        self.assertCountEqual(response.data, parkruns_data)

    def test_post_to_event_list_gets_405(self):
        response = self.client.post(
            "/events/",
            data={
                "country": 1,
                "name": "Toolazytolookoneup",
                "slug": "toolazytolookoneup",
                "latitude": 0,
                "longitude": 0
            }
        )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def tearDown(self):
        pass
