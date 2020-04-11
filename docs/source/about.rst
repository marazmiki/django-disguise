About
=====

This application allows a site superuser (or some staff user authorized for the action)
to *disguise* into an arbitrary user **without knowing its password and without losing the original session**.

Features
--------

* work on each page
* user_sign_in signal ignore
* solid interface
* handy configurable widget
* customized permission checker
* easy to extend with working with ajax or websocket

BTW, why "disguise"?
--------------------

Have you ever play in `Team Fortress <https://teamfortress.com>`_? If so,
perhaps, I should not answer the question, you've already got it. If you haven't,
well, will try to explain.

**Team Fortress** is a first-person role shooter. `Role` means you can choose one of a few user classes
having own abilities, e.g.

* ``Medic`` can repair damages,
* ``Scout`` runs so fast
* ``Sniper`` has a rifle...

Also, there is a wonderful player class called ``Spy``, who has the ability
to take the shape of any other class. Everybody sees a running blue scout while
actually it's a Red Spy.

You can view a short movie, it's quite funny.

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/OR4N5OhcY9s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

So, this skill called **disguise**. And I found this application makes a site superuser into a spy who can acts like a regular user, even without knowing the password.


Competitors
-----------

