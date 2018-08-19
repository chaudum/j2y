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

Local Development
-----------------

Bootstrapping
.............

Create a virtualenv and install the package as develop egg::

  $ python -m venv env
  $ env/bin/activate
  (env) $ pip install -e .

Tests
.....

At the moment there are very simple test cases only. Test are written as native
Python doctests. You can invoke them like so::

  (env) $ python j2y/tests.py
