=====
Usage
=====

To use parkrundata in a project, add it to your `INSTALLED_APPS`:

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
