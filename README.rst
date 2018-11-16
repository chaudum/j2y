j2y - A Jinja2 Template CLI
===========================

.. image:: https://travis-ci.org/chaudum/j2y.svg?branch=master
    :target: https://travis-ci.org/chaudum/j2y
    :alt: Travis CI

.. image:: https://badge.fury.io/py/j2y.svg
    :target: http://badge.fury.io/py/j2y
    :alt: Python Package Index

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code Style: Black

|

Render Jinja2 templates on the command line using a YAML_, JSON_ or HCL_ file
as input for the render context.

💽 Installation
--------------

``j2y`` is installed using ``pip``::

  $ pip install j2y

Alternatively you can install directly from Github master branch::

  $ pip install git+https://github.com/chaudum/j2y.git@master

👩‍💻 Usage
---------

By default, ``j2y`` takes a YAML_ file as input::

  $ j2y template.j2 < values.yaml

Alternatively you can use JSON_ or HCL_ as input format::

  $ j2y template.j2 -f json < values.json
  $ j2y template.j2 -f hcl < values.hcl

It's also possible to provide multiple input files::

  $ j2y template.j2 --context v1.yaml --context v2.yaml

Run ``j2y -h`` to see all available options.

Template Variables
..................

Additionally to the variables provided by the input file, ``j2y`` also provides
built-in default variables. These variables are:

:meta.date:
  Type:  ``datetime``

  Value: Current UTC datetime object

:meta.platform:
  Type:  ``dict``

  Value: Output of ``platform.uname()``

:env:
  Type:  ``dict``

  Value: All environment variables (output of ``os.environ``).

⚗️ Local Development
-------------------

Bootstrapping
.............

Create a virtualenv_ and install the package as develop egg::

  $ python -m venv env
  $ source env/bin/activate
  (env) $ pip install -e .

Tests
.....

At the moment there are very simple test cases only. Test are written as
Python doctests and run using `pytest`_::

  (env) $ pip install -e ".[test]"
  (env) $ pytest

Pytest additionally runs the `black`_ linter and `mypy`_ static type checker.

The tests located in the ``docs/`` folder can also be built into HTML using
`Sphinx`_::

  (env) $ sphinx-build -E -W docs/ _build/


.. _YAML: http://yaml.org/spec/
.. _JSON: https://www.json.org/
.. _HCL: https://github.com/hashicorp/hcl
.. _virtualenv: https://docs.python.org/3/tutorial/venv.html
.. _pytest: https://docs.pytest.org/en/latest/
.. _black: https://github.com/ambv/black
.. _mypy: https://github.com/python/mypy
.. _Sphinx: http://www.sphinx-doc.org/en/master/
