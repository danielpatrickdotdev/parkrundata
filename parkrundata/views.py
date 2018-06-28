# -*- coding: utf-8 -*-

from django.http import Http404

from rest_framework import viewsets, generics

from .models import Country, Event
from .serializers import CountrySerializer, EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_object(self):
        """
        Override existing generics.GenericAPIView method to allow retrieving
        Event objects by country.name and event.name
        """
        queryset = self.filter_queryset(self.get_queryset())

        url = self.kwargs["url"]
        try:
            country_url, slug = url.split("/")
        except:
            raise Http404

        filter_kwargs = {
            "country__url": country_url,
            "slug": slug
        }
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
