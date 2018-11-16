==================
Template Rendering
==================

.. hidden: Global imports

  >>> import os
  >>> import tempfile
  >>> from pathlib import Path

Setup environment::

  >>> from j2cli.cli import create_environment, render_template

  >>> tpl = tempfile.NamedTemporaryFile()
  >>> os.chdir(Path(tpl.name).parent)
  >>> env = create_environment(Path.cwd())

Create template::

  >>> tpl.write('Hello {{ name }}!'.encode('utf-8'))
  17
  >>> tpl.flush()

Render template with context::

  >>> render_template(
  ...     Path(tpl.name).relative_to(Path.cwd()),
  ...     env,
  ...     {'name': 'World'}
  ... )
  'Hello World!'
