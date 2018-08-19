#!/usr/bin/env python3
"""
j2y - a super simple Jinja2 templating command line interface
"""

import io
import os
import sys
import json
import yaml
import shutil
import argparse
import platform
import functools

from datetime import datetime

from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from typing import Any, Dict, Tuple, List


p_err = functools.partial(print, file=sys.stderr)
p_out = functools.partial(print, file=sys.stdout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('template',
                        type=Path,
                        help='path of the Jinja template')
    parser.add_argument('-c', '--context',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='input file for template context, defaults to stdin')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='output file, defaults to stdout')
    parser.add_argument('-f', '--format',
                        choices=['yaml', 'json'],
                        default='yaml',
                        help='input file format')
    parser.add_argument('-x', '--extra', action="append",
                        default=[],
                        help='provide extra variables for template context via cli using key=value pair')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='print template context to stderr')
    return parser.parse_args()


def parse_extra(extra: List[str]) -> Dict:
    return dict(x.split('=') for x in extra)


def get_template(path: Path, env: Environment) -> Template:
    return env.get_template(str(path))


def load_context(fp: io.TextIOWrapper, loader: callable) -> Dict[str, Any]:
    return loader(fp) or {}


def loaders() -> Dict[str, callable]:
    return {
        'yaml': lambda fp: yaml.load(fp.read()),
        'json': lambda fp: json.load(fp),
    }


def get_loader(format: str) -> callable:
    return loaders()[format]


def create_environment(path: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(path.absolute()))
    )


def render_template(template: Path,
                    env: Environment,
                    context: Dict[str, Any],
                    output: io.TextIOWrapper) -> None:
    tpl = get_template(template, env)
    output.write(tpl.render(**context))
    output.write('\n')
    output.flush()


def default_context() -> Dict[str, Any]:
    return {
        "meta": {
            "date": datetime.utcnow(),
            "platform": dict(platform.uname()._asdict())
        }
    }


def tty_size() -> Tuple[int, int]:
    return shutil.get_terminal_size((20, 1))


def print_context(ctx: Dict[str, Any], width: int = 12) -> None:
    p_err(yaml.dump(ctx, default_flow_style=False, indent=2, width=width))
    p_err("=" * width)
    p_err("")


def main():
    args = parse_args()
    extra = parse_extra(args.extra)
    env = create_environment(Path(os.path.curdir))
    ctx = default_context()
    ctx.update(load_context(args.context, get_loader(args.format)))
    ctx.update(extra)
    if args.verbose:
        print_context(ctx, tty_size()[0])
    render_template(args.template, env, ctx, args.output)
