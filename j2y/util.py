import sys
import shutil
import functools

from typing import Dict, List, Tuple, cast


print_stderr = functools.partial(print, file=sys.stderr)


def parse_extra(extra: List[str]) -> Dict[str, str]:
    return dict(cast(Tuple[str, str], x.split("=", 1)) for x in extra)


def tty_size() -> Tuple[int, int]:
    return shutil.get_terminal_size((20, 1))
