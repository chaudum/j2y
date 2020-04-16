"""
j2y - a super simple Jinja2 templating command line interface
"""

import os
import sys
import hcl
import json
import yaml
import argparse
import platform

from datetime import datetime

from pathlib import Path
from typing import Any, Callable, Dict, List, TextIO
from jinja2 import Environment, FileSystemLoader

from j2cli.util import parse_extra, tty_size, print_stderr
from j2cli.filters import registry as filter_registry


# fmt: off
def parse_args(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="j2cli",
        description=__doc__,
    )
    parser.add_argument(
        "template",
        type=Path,
        help="Path to the Jinja2 template file."
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


def load_contexts(fps: List[TextIO], loader: Callable) -> Dict[str, Any]:
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
    tpl = env.get_template(str(template))
    return tpl.render(**context)


def write(output: str, fd: TextIO) -> None:
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


def entrypoint(
    template: str,
    output: TextIO,
    *,
    contexts: List[TextIO] = None,
    extra: List[str] = None,
    format: str = "yaml",
    verbose: bool = False,
) -> None:
    extras = parse_extra(extra or [])
    template_path = Path(template)
    env = create_environment(template_path.parent)
    ctx = default_context()

    if not contexts:
        print_stderr("stdin as default value for --context argument is deprecated.")
        print_stderr("Please specify -c or --context explicitly, e.g. `-c -`")
        contexts = [sys.stdin]

    ctx.update(load_contexts(contexts, get_loader(format)))
    ctx.update(extras)
    if verbose:
        print_context(ctx, tty_size()[0])
    relative_template_path = template_path.relative_to(template_path.parent)
    write(render_template(relative_template_path, env, ctx), output)


def main_deprecated() -> None:
    print_stderr(
        "\033[31m"
        "The command 'j2y' command is deprecated. Please use 'j2cli' instead."
        "\033[0m"
    )
    main()


def main() -> None:
    args = parse_args(sys.argv[1:])
    entrypoint(
        args.template,
        args.output,
        contexts=args.context,
        extra=args.extra,
        format=args.format,
        verbose=args.verbose,
    )
