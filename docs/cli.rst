======================
Command Line Arguments
======================

.. hidden: Global imports

  >>> import io
  >>> import os
  >>> import sys
  >>> import tempfile

::

  >>> from j2y.cli import parse_args

The following CLI argument tests require a helper function so we can read the
output of ``argparse.ArgumentParser.parse_args()`` correctly.

::

  >>> def parse_args_safe(args):
  ...     sys.argv[0] = "j2y"
  ...     stderr = sys.stderr
  ...     sys.stderr = io.StringIO()
  ...     try:
  ...         return parse_args(args)
  ...     except SystemExit as e:
  ...         return sys.stderr.getvalue()
  ...     finally:
  ...         sys.stderr = stderr

Argument Parsing
================

Parse program invokation without arguments::

  >>> out = parse_args_safe([])
  >>> print(out)
  usage: j2y [-h] [-c CONTEXT] [-o OUTPUT] [-f {yaml,json,hcl}] [-x EXTRA] [-v]
             template
  j2y: error: the following arguments are required: template

Parse default arguments::

  >>> args = parse_args_safe(['template.j2'])
  >>> args.template
  PosixPath('template.j2')
  >>> args.context
  []
  >>> args.extra
  []
  >>> args.format
  'yaml'
  >>> args.verbose
  False

Change ``format`` and ``verbose``::

  >>> args = parse_args_safe(['template.j2', '-f', 'json', '-v'])
  >>> args.format
  'json'
  >>> args.verbose
  True

Change output file::

  >>> args = parse_args_safe(['template.j2', '-o', 'outfile'])
  >>> args.output
  <_io.TextIOWrapper name='outfile' mode='w' encoding='UTF-8'>

.. hidden: Remove output

   >>> args.output.close()
   >>> os.unlink(args.output.name)

Provide input file, however, it needs to exist::

  >>> with tempfile.NamedTemporaryFile() as infile:
  ...     args = parse_args_safe(['template.j2', '-c', infile.name])
  ...     print(args.context)
  ...     print(args.context[0].name == infile.name)
  [<_io.TextIOWrapper name='...' mode='r' encoding='UTF-8'>]
  True
