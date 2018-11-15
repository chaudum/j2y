=========
Changelog
=========

Unreleased
==========

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
