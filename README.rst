j2y - A Jinja2 Template CLI
===========================

Render Jinja2 templates on the command line using a YAML file as input for
the render context.

Installation
------------

``j2y`` can be installed using ``pip``::

  pip install git+https://github.com/chaudum/j2y.git@master

Usage
-----

By default, ``j2y`` takes a ``YAML`` file as input::

  j2y template.j2 < values.yaml

Alternatively you can use JSON as input format::

  j2y template.j2 -f json < values.json


Run ``j2y -h`` to see all available options.
