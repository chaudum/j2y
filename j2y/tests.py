import doctest


if __name__ == "__main__":
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.FAIL_FAST
    doctest.testfile("cli.rst", optionflags=flags)
