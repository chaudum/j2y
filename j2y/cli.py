#!/usr/bin/env python3
"""

j2y - a super simple Jinja2 command line interface

Example usage::

    >>> cat values.yaml
    name: christian

    >>> cat template.j2
    Hello {{ name | upper }}!

    >>> j2y template.j2 < values.yaml
    Hello CHRISTIAN!

"""

import io
import os
import sys
import json
import yaml
import argparse

from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from typing import Any, Dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Jinja2 CLI')
    parser.add_argument('template',
                        type=Path,
                        help='path of the template')
    parser.add_argument('-c', '--context',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='input file, defaults to stdin')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='output file, defaults to stdout')
    parser.add_argument('-f', '--format',
                        choices=['yaml', 'json'],
                        default='yaml',
                        help='input file format')
    return parser.parse_args()


def get_template(path: Path, env: Environment) -> Template:
    return env.get_template(str(path))


def load_context(fp: io.TextIOWrapper, loader: callable) -> Dict[str, Any]:
    return loader(fp)


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


def main():
    args = parse_args()
    env = create_environment(Path(os.path.curdir))
    ctx = load_context(args.context, get_loader(args.format))
    render_template(args.template, env, ctx, args.output)
