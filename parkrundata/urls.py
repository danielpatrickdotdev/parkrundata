# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework.routers import Route, SimpleRouter

from . import views


app_name = 'parkrundata'

router = SimpleRouter()
router.register("events", views.EventViewSet)
urlpatterns = router.urls
