import sys
import shutil
import functools

from typing import Dict, List, Tuple


print_stderr = functools.partial(print, file=sys.stderr)


def parse_extra(extra: List[str]) -> Dict:
    return dict(x.split('=') for x in extra)


def tty_size() -> Tuple[int, int]:
    return shutil.get_terminal_size((20, 1))
