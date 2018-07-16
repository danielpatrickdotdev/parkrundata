#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` views module.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from parkrundata import models, views


User = get_user_model()


class TestEventViewSetBase(APITestCase):

    def setUp(self):
        self.uk = models.Country.objects.create(
                name="UK", url="http://www.parkrun.org.uk")
        self.france = models.Country.objects.create(
                name="France", url="http://www.parkrun.fr")
        self.germany = models.Country.objects.create(
                name="Germany", url="http://www.parkrun.com.de")

        self.bushy = models.Event.objects.create(
            country=self.uk,
            name="Bushy",
            slug="bushy",
            latitude="51.4096938",
            longitude="-0.3340315"
        )

        self.lesdougnes = models.Event.objects.create(
            country=self.france,
            name="Les Dougnes",
            slug="lesdougnes",
            latitude="45.066553",
            longitude="-0.429266"
        )

        self.neckarau = models.Event.objects.create(
            country=self.germany,
            name="Neckarau",
            slug="neckarau",
            latitude="49.448549",
            longitude="8.453786"
        )

        self.factory = APIRequestFactory()

    def tearDown(self):
        pass


class TestEventViewSetWithoutAuthentication(TestEventViewSetBase):
    """
    Tests that need to be executed by AnonymousUser
    """

    def setup_view(self, request=None, url=None, args=None, kwargs=None):
        view = views.EventViewSet()
        view.request = request or self.factory.get(url or "")
        view.args = args
        view.kwargs = kwargs
        return view

    def test_retrieve_event(self):
        view = self.setup_view(kwargs={"pk": 1})
        obj = view.get_object()

        self.assertEqual(obj, self.bushy)

    def test_retrieves_event_as_json(self):
        response = self.client.get("/events/1/")
        self.assertEqual(response.accepted_media_type, "application/json")

    def test_retrieve_event_list(self):
        view = self.setup_view()
        events = view.get_queryset()
        self.assertCountEqual(events,
                              [self.bushy, self.lesdougnes, self.neckarau])

    def test_invalid_pk_raises_404(self):
        for pk in [0, 4]:
            view = self.setup_view(kwargs={"pk": pk})
            with self.assertRaises(Http404):
                view.get_object()

    def test_cannot_create_event_unless_authenticated(self):
        response = self.client.post("/events/", {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_modify_event_unless_authenticated(self):
        response = self.client.put("/events/1/", {"name": "Bushy Park"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_event_unless_authenticated(self):
        response = self.client.delete("/events/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestEventViewSetWithAuthentication(TestEventViewSetBase):
    """
    Tests that need to be executed by authenticated User
    """

    def setUp(self):
        self.user = User.objects.create(username="test")
        self.client.force_authenticate(user=self.user)

        super().setUp()

    def test_create_event(self):
        new_event_data = {
            "country": self.uk.id,
            "name": "New Event",
            "slug": "newevent",
            "latitude": "1.234567",
            "longitude": "-1.234567"
        }
        response = self.client.post("/events/", new_event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_event = models.Event.objects.get(id=4)
        self.assertEqual(new_event.country, self.uk)
        self.assertEqual(new_event.name, "New Event")
        self.assertEqual(new_event.slug, "newevent")
        self.assertEqual(new_event.latitude, Decimal("1.234567"))
        self.assertEqual(new_event.longitude, Decimal("-1.234567"))

    def test_modify_event(self):
        data = {
            "country": self.germany.id,
            "name": "Bushy Park",
            "slug": "bushypark",
            "latitude": "0.123456",
            "longitude": "-0.123456"
        }

        response = self.client.put("/events/1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event = models.Event.objects.get(id=1)
        self.assertEqual(event.country, self.germany)
        self.assertEqual(event.name, "Bushy Park")
        self.assertEqual(event.slug, "bushypark")
        self.assertEqual(event.latitude, Decimal("0.123456"))
        self.assertEqual(event.longitude, Decimal("-0.123456"))

    def test_partially_modify_event(self):
        data = {
            "country": self.germany.id,
        }

        response = self.client.patch("/events/1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event = models.Event.objects.get(id=1)
        self.assertEqual(event.country, self.germany)
        self.assertEqual(event.name, "Bushy")
        self.assertEqual(event.slug, "bushy")
        self.assertEqual(event.latitude, Decimal("51.409694"))
        self.assertEqual(event.longitude, Decimal("-0.334032"))

    def test_delete_event(self):
        response = self.client.delete("/events/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(models.Event.DoesNotExist):
            models.Event.objects.get(id=1)
