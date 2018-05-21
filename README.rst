=============================
parkrundata
=============================

Django app for storing parkrun data

Quickstart
----------

Install parkrundata::

    pip install parkrundata

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'parkrundata.apps.ParkrundataConfig',
        ...
    )

Add parkrundata's URL patterns:

.. code-block:: python

    from parkrundata import urls as parkrundata_urls


    urlpatterns = [
        ...
        url(r'^', include(parkrundata_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
