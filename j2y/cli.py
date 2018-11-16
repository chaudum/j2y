"""
j2y - a super simple Jinja2 templating command line interface
"""

import io
import os
import sys
import hcl
import json
import yaml
import argparse
import platform

from datetime import datetime

from pathlib import Path
from typing import Any, Callable, Dict, List
from jinja2 import Template, Environment, FileSystemLoader

from j2y.util import parse_extra, tty_size, print_stderr
from j2y.filters import registry as filter_registry


# fmt: off
def parse_args(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "template",
        type=Path,
        help="Path to the Jinja template file."
    )
    parser.add_argument(
        "-c",
        "--context",
        type=argparse.FileType("r"),
        default=[],
        action="append",
        help="Path to the input file that serves as source for the render context"
        "of the Jinja template. This argument may be specified multiple times.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Path to the output file to which the rendered Jinja template is written"
        "to. If the argument is omitted, j2y will print stdout.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=loaders().keys(),
        default="yaml",
        help="File format of the input file(s) specified with --context."
        " If multiple input files where specified they need to have the same file"
        " format",
    )
    parser.add_argument(
        "-x",
        "--extra",
        action="append",
        default=[],
        help="Provide an additional variable for the Jinja template render context."
        " The value of this argument needs to provided as key=value pair."
        " This argument may be specified multiple times."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the Jinja template render context prior to the rendered template."
        " The render context is printed to stdout."
    )
    return parser.parse_args(arguments)
# fmt: on


def get_template(path: Path, env: Environment) -> Template:
    return env.get_template(str(path))


def load_contexts(fps: List[io.TextIOWrapper], loader: Callable) -> Dict[str, Any]:
    context: Dict = {}
    for fp in fps:
        context.update(loader(fp) or {})
    return context


def loaders() -> Dict[str, Callable]:
    return {
        "yaml": lambda fp: yaml.load(fp.read()),
        "json": lambda fp: json.load(fp),
        "hcl": lambda fp: hcl.load(fp),
    }


def get_loader(format: str) -> Callable:
    return loaders()[format]


def create_environment(path: Path) -> Environment:
    env = Environment(loader=FileSystemLoader(str(path.absolute())))
    env.filters.update(filter_registry)
    return env


def render_template(template: Path, env: Environment, context: Dict[str, Any]) -> str:
    tpl = get_template(template, env)
    return tpl.render(**context)


def write(output: str, fd: io.TextIOWrapper) -> None:
    fd.write(output)
    fd.write("\n")
    fd.flush()


def default_context() -> Dict[str, Any]:
    return {
        "meta": {
            "date": datetime.utcnow(),
            "platform": dict(platform.uname()._asdict()),
        },
        "env": dict(os.environ),
    }


def print_context(ctx: Dict[str, Any], width: int = 12) -> None:
    print_stderr(yaml.dump(ctx, default_flow_style=False, indent=2, width=width))
    print_stderr("=" * width)
    print_stderr("")


def entrypoint(args: argparse.Namespace) -> None:
    extra = parse_extra(args.extra)
    env = create_environment(Path(os.path.curdir))
    ctx = default_context()
    ctx.update(load_contexts(args.context, get_loader(args.format)))
    ctx.update(extra)
    if args.verbose:
        print_context(ctx, tty_size()[0])
    write(render_template(args.template, env, ctx), args.output)


def main() -> None:
    entrypoint(parse_args(sys.argv[1:]))
