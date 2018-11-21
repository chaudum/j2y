=========
Changelog
=========

Unreleased
==========

2018/11/21 0.2.1
================

- *[FIX]* Fix the behaviour of the default input that broke with the
  introduction of multiple input files. It is now possible again to redirect
  stdin to the command without specifying the ``-c/--context`` argument, such
  as ``j2y template.j2 < values.yaml``. Default stdin is ignored, however, if
  additional input files are provided.

2018/11/18 0.2.0
================

- *[FEATURE]* Add serialization functions ``json`` and ``yaml`` as template
  filters.

- *[FEATURE]* Add support for multiple input files using the ``-c`` or
  ``--context`` argument.

- *[FEATURE]* Add hashlib digest functions ``md5sum``, ``sha1sum``,
  ``sha256sum`` and ``sha512sum`` as template filters.

- *[FEATURE]* Provide environment variables as template variable ``env``.

2018/10/23 0.1.0
================

- *[FEATURE]* Add Base64 template filters (``b64encode``, ``b64decode``).

- *[FEATURE]* Add support for the `HCL <https://github.com/hashicorp/hcl>`_
  file format as input file.

- *[FEATURE]* Initial feature set with YAML and JSON file format as input file.
