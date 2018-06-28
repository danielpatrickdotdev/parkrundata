# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework.routers import Route, SimpleRouter

from . import views


app_name = 'parkrundata'

class ReadOnlyRouter(SimpleRouter):

    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        Route(
            url=r"^{prefix}/{lookup}/$",
            mapping={"get": "retrieve"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"}
        )
    ]

router = ReadOnlyRouter()
router.register("events", views.EventViewSet)
urlpatterns = router.urls
