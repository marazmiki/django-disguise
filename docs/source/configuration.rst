Configuration
=============

Settings
--------

.. code:: python

    # settings.py
    INSTALLED_APPS = [
        # ...apps
        'disguise',
        # ...another apps
    ]

Add the ``disguise.middleware.DisguiseMiddleware`` to the ``MIDDLEWARE`` list in your ``settings`` module.
Make sure ``django.contrib.sessions.middleware.SessionMiddleware`` in there and follow before the disguise middleware.

.. code:: python

    # settings.py
    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'disguise.middleware.DisguiseMiddleware'

    ]

Here you can see an example of overriding of the default behavior

.. code:: python

    # settings.py
    DISGUISE = {
        'can_disguise': 'my_project.utils.my_own_can_disguise',
        'widget_form': 'my_project.utils.MyOwnDisguiseWidgetForm',
    }


urls.py
-------

.. code:: python



    # urls.py
    from django.urls import include, path

    urlpatterns = [
        #...
        path('disguise/', include('disguise.urls')),


migration
---------

.. code:: bash

    $ manage.py migrate
