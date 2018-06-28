#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parkrundata
------------

Tests for `parkrundata` views module.
"""

from django.http import Http404
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from parkrundata import models, views


class TestEventViewSet(TestCase):

    def setUp(self):
        self.uk = models.Country.objects.create(
                name="UK", url="www.parkrun.org.uk")
        self.france = models.Country.objects.create(
                name="France", url="www.parkrun.fr")
        self.germany = models.Country.objects.create(
                name="Germany", url="www.parkrun.com.de")

        self.bushy = models.Event.objects.create(
            country = self.uk,
            name = "Bushy",
            slug = "bushy",
            latitude = "51.4096938",
            longitude = "-0.3340315"
        )

        self.lesdougnes = models.Event.objects.create(
            country = self.france,
            name = "Les Dougnes",
            slug = "lesdougnes",
            latitude = "45.066553",
            longitude = "-0.429266"
        )

        self.neckarau = models.Event.objects.create(
            country = self.germany,
            name = "Neckarau",
            slug = "neckarau",
            latitude = "49.448549",
            longitude = "8.453786"
        )

        self.factory = APIRequestFactory()

    def setup_view(self, request, args=None, kwargs=None):
        view = views.EventViewSet()
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_retrieve_event(self):
        request = self.factory.get("")
        view = self.setup_view(request, kwargs={"pk": 1})
        obj = view.get_object()

        self.assertEqual(obj, self.bushy)

    def test_retrieve_event_list(self):
        request = self.factory.get("")
        view = self.setup_view(request)
        events = view.get_queryset()
        self.assertCountEqual(events,
                              [self.bushy, self.lesdougnes, self.neckarau])

    def test_invalid_pk_raises_404(self):

        for pk in [0, 4]:
            request = self.factory.get("")
            view = self.setup_view(request, kwargs={"pk": pk})
            with self.assertRaises(Http404):
                obj = view.get_object()

    def tearDown(self):
        pass
