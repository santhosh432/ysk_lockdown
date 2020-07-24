YSK lock down to make user lock

YSK_DJANGO_LOCK-DOWN
===============

This is a django application for user lock down after 5 incorrect attempts.

Installable App
---------------

This app models a list of items on a lockdown.
This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install pip install ysk-django-lockdown


Edit your `settings.py` file to include `'lockdown'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        'lockdown',
    ]


Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('lockdown/', include('lockdown.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py makemigrations lockdown


The "project" Branch
--------------------

The `master branch <https://github.com/santhosh432/ysk_lockdown>`_ contains the final code for the PyPI package. There is also a `project branch <https://github.com/realpython/django-receipts/tree/project>`_ which shows the "before" case -- the Django project before the app has been removed.


Docs & Source
-------------


* Source: https://github.com/santhosh432/ysk_lockdown
* PyPI: https://pypi.org/project/ysk-django-lockdown/
