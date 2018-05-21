# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import Country, Event


class CountryDetailView(DetailView):

    model = Country


class CountryListView(ListView):

    model = Country


class EventDetailView(DetailView):

    model = Event


class EventListView(ListView):

    model = Event
