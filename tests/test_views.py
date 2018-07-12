#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` views module.
"""

from django.http import Http404

from rest_framework.test import APIRequestFactory, APITestCase

from parkrundata import models, views


class TestEventViewSetBase(APITestCase):

    def setUp(self):
        self.uk = models.Country.objects.create(
                name="UK", url="www.parkrun.org.uk")
        self.france = models.Country.objects.create(
                name="France", url="www.parkrun.fr")
        self.germany = models.Country.objects.create(
                name="Germany", url="www.parkrun.com.de")

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

    def setup_view(self, request=None, url=None, args=None, kwargs=None):
        view = views.EventViewSet()
        view.request = request or self.factory.get(url or "")
        view.args = args
        view.kwargs = kwargs
        return view

    def tearDown(self):
        pass


class TestEventViewSetWithoutAuthentication(TestEventViewSetBase):
    """
    Tests that need to be executed by AnonymousUser
    """

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
        pass

    def test_cannot_modify_event_unless_authenticated(self):
        pass

    def test_cannot_delete_event_unless_authenticated(self):
        pass


class TestEventViewSetWithAuthentication(TestEventViewSetBase):
    """
    Tests that need to be executed by authenticated User
    """

    def test_create_event(self):
        pass

    def test_modify_event(self):
        pass

    def test_delete_event(self):
        pass
