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


class TestCountryURLs(TestCase):

    def setUp(self):
        self.uk_data = {"name": "UK", "url": "www.parkrun.org.uk"}
        self.france_data = {"name": "France", "url": "www.parkrun.fr"}
        self.germany_data = {
            "name": "Germany", "url": "www.parkrun.com.de"}

        self.uk = models.Country.objects.create(**self.uk_data)
        self.france = models.Country.objects.create(**self.france_data)
        self.germany = models.Country.objects.create(**self.germany_data)

        self.uk_data["id"] = 1
        self.france_data["id"] = 2
        self.germany_data["id"] = 3

    def test_retrieve_country_returns_correct_object(self):
        response = self.client.get("/countries/1/", format="json")
        self.assertEqual(response.data, self.uk_data)

    def test_retrieve_country_incorrect_url_gets_404(self):
        response = self.client.get("/countries/4/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_country_gets_403(self):
        response = self.client.patch("/countries/1/", data={"name": "USA"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_country_gets_403(self):
        response = self.client.delete("/countries/1/")
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_retrieve_country_list(self):
        response = self.client.get("/countries/")
        countries_data = [
            self.uk_data, self.france_data, self.germany_data]
        self.assertCountEqual(response.data, countries_data)

    def test_post_to_country_list_gets_403(self):
        response = self.client.post(
            "/countries/",
            data={"name": "USA", "url": "http://www.parkrun.us"}
        )
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        pass


class TestEventURLs(TestCase):

    def setUp(self):
        self.bool_defaults = {
            "is_juniors": False,
            "is_restricted": False,
            "is_discontinued": False,
        }

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
        self.bushy_data["id"] = self.bushy_data["country"] = 1
        self.bushy_data.update(self.bool_defaults)

        self.lesdougnes_data = {
            "country": self.france,
            "name": "Les Dougnes",
            "slug": "lesdougnes",
            "latitude": "45.066553",
            "longitude": "-0.429266"
        }
        self.lesdougnes = models.Event.objects.create(**self.lesdougnes_data)
        self.lesdougnes_data["id"] = self.lesdougnes_data["country"] = 2
        self.lesdougnes_data.update(self.bool_defaults)

        self.neckarau_data = {
            "country": self.germany,
            "name": "Neckarau",
            "slug": "neckarau",
            "latitude": "49.448549",
            "longitude": "8.453786"
        }
        self.neckarau = models.Event.objects.create(**self.neckarau_data)
        self.neckarau_data["id"] = self.neckarau_data["country"] = 3
        self.neckarau_data.update(self.bool_defaults)

        self.client = APIClient()

    def test_retrieve_event_returns_correct_object(self):
        response = self.client.get("/events/1/", format="json")
        bushy_data = self.bushy_data
        self.assertEqual(response.data, bushy_data)

    def test_retrieve_event_incorrect_url_gets_404(self):
        response = self.client.get("/events/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_event_gets_403(self):
        response = self.client.post("/events/1/", data={"name": "Bushy Park"})
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_delete_event_gets_403(self):
        response = self.client.delete("/events/1/")
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_retrieve_event_list(self):
        response = self.client.get("/events/")
        parkruns_data = [
            self.bushy_data, self.lesdougnes_data, self.neckarau_data]
        self.assertCountEqual(response.data, parkruns_data)

    def test_post_to_event_list_gets_403(self):
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
                         status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        pass
