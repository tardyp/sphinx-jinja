Header level tests
==================

First, render without the ``header_update_levels`` option:

.. jinja::

   same style, but second level
   ============================

   Above header is a second-level header, since all headers will be in levels
   below the active level header of the caller.

   ************************
   New style is third level
   ************************

   A new style will go to an even lower level.

Next, try to render with the ``header_update_levels`` option:

.. jinja::
   :header_update_levels:

   same style, same level
   ======================

   Because of the ``header_update_levels`` option, the same header style means
   the same header level (like with the ``include`` directive).

   ************
   Second level
   ************

   A level two section (because this is the first time this style occcurs).

