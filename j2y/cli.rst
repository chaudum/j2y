=====
Tests
=====

Global imports::

  >>> import io
  >>> import os
  >>> import sys
  >>> import tempfile
  >>> from pathlib import Path

Argument Parsing
================

Setup::

  >>> stderr = sys.stderr
  >>> mock_stderr = io.StringIO()
  >>> sys.stderr = mock_stderr

  >>> from j2y.cli import parse_args

Helper function to parse arguments safely::

  >>> def parse_args_safe(args):
  ...     mock_stderr.truncate(0)
  ...     sys.argv = args
  ...     try:
  ...         return parse_args()
  ...     except SystemExit as e:
  ...         pass
  ...     finally:
  ...         sys.argv = []
  ...     return mock_stderr.getvalue()

Parse program invokation without arguments::

  >>> out = parse_args_safe(['j2y'])
  >>> print(out)
  usage: j2y [-h] [-c CONTEXT] [-o OUTPUT] [-f {yaml,json,hcl}] [-x EXTRA] [-v]
             template
  j2y: error: the following arguments are required: template

Parse default arguments::

  >>> args = parse_args_safe(['j2y', 'template.j2'])
  >>> args.template
  PosixPath('template.j2')
  >>> args.context
  <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>
  >>> args.extra
  []
  >>> args.format
  'yaml'
  >>> args.verbose
  False

Change ``format`` and ``verbose``::

  >>> args = parse_args_safe(['j2y', 'template.j2', '-f', 'json', '-v'])
  >>> args.format
  'json'
  >>> args.verbose
  True

Change output file::

  >>> args = parse_args_safe(['j2y', 'template.j2', '-o', 'outfile'])
  >>> args.output
  <_io.TextIOWrapper name='outfile' mode='w' encoding='UTF-8'>

Provide input file, however, it needs to exist::

  >>> with tempfile.NamedTemporaryFile() as infile:
  ...     args = parse_args_safe(['j2y', 'template.j2', '-c', infile.name])
  ...     print(args.context)
  ...     print(args.context.name == infile.name)
  <_io.TextIOWrapper name='...' mode='r' encoding='UTF-8'>
  True

Template Rendering
==================

Setup environment::

  >>> from j2y.cli import create_environment, render_template

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
