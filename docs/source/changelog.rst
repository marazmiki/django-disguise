Change log
==========

1.x
---


1.2
~~~

* Added support for ``Django 4.x`` and ``Python 3.10``
* Dropped support for ``Python 3.5`` and older
* Get rid of Travis CI in favor of GitHub Actions
* Updated test dependencies

1.0.1
~~~~~

* Added form errors handling
* Fixed a bug when trying to switch a disabled user
* Updated ``RU`` locales

1.0.0
~~~~~

* Using ``poetry`` to build the package;
* Support for ``Python 2.7`` and ``Python 3.4+``;
* Support for ``Django 1.11``, ``Django 2.x`` and ``Django 3.x``;
* Use ``pytest`` for tests;
* Added a project configuration self checking mechanism using the  ``Django``'s ``check`` framework;
* Make the app configurable (able to customize a widget form and ``can_disguise`` behavior);
* Changed signal names and signatures to more suitable;
* Does not send ``user_logged_in`` signal when swapping a user;
* Changed the license from ``BSD`` to ``MIT``.

0.x
---

0.2.3
~~~~~

* Use ``tox`` for testing
* Drop support for ``Django==1.4``

0.2.2
~~~~~

* Update head django==1.8 version

0.2.1
~~~~~

* Update head django versions

0.2
~~~

* Add django 1.8 support

0.1
~~~

* Permissions for disguise now linked with User model;
* Using django system check framework in newest versions;
* Disguise widget become a template tag; earlier it added into page with middleware;
* Migrated to CBV views;
* Code imporvements (pep8);
* Added coverage support;
* Added signals;
* Removed the ``update_user_login`` feature prior to custom signal handling;


0.0.3
~~~~~

* Travis CI integration
