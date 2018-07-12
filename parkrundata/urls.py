# -*- coding: utf-8 -*-

from rest_framework.routers import SimpleRouter

from . import views


app_name = 'parkrundata'

router = SimpleRouter()
router.register("events", views.EventViewSet)
urlpatterns = router.urls
