# -*- coding: utf-8 -*-

from django.http import Http404

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Country, Event
from .serializers import CountrySerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
