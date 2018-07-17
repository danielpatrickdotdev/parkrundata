# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import TimeStampedModel


class Country(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField()


class Event(TimeStampedModel):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = (
            ("country", "name"),
            ("country", "slug"),
        )
