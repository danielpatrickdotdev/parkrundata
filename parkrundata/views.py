# -*- coding: utf-8 -*-

from django.http import Http404

from rest_framework import viewsets, generics

from .models import Country, Event
from .serializers import CountrySerializer, EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
