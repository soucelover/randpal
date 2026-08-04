from __future__ import annotations

import inspect
from argparse import (
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
    _SubParsersAction,
)
from collections.abc import Callable, Sequence
from typing import TypeAlias

import randpal
from randpal.__main__ import command_choose, command_int

CommandFunction: TypeAlias = Callable[[Namespace], None]


def get_docs_header(obj: object) -> tuple[str, str] | tuple[None, None]:
    """Get header of object's docstring.

    Args:
        obj: Source of docstring.

    Returns:
        The first line of the dosctring and an original docstring itself.
    """
    docs = inspect.getdoc(obj)

    if docs is None:
        return None, None

    header, _, _body = docs.partition("\n")
    return header, docs


def add_command(  # noqa: PLR0913
    commands: _SubParsersAction[ArgumentParser],
    name: str,
    function: CommandFunction,
    *,
    help: str | None = None,  # noqa: A002
    epilog: str | None = None,
    aliases: Sequence[str] = (),
) -> ArgumentParser:
    """Register a single command in `SubParsersAction`.

    Args:
        commands: `ArgumentParser`'s action representing commands
        name: Name for the command.
        function: Function implementing command and containing its docstrings.
        aliases: Optional list of aliases for the command.

    Returns:
        A newly created parser of the command.
    """
    header, docs = get_docs_header(function)

    if help is None:
        help = header  # noqa: A001

    parser = commands.add_parser(
        name,
        help=help,
        description=docs,
        epilog=epilog,
        aliases=aliases,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.set_defaults(command=function)
    return parser


def register_commands(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)

    com_int = add_command(commands, "int", command_int)
    com_int.add_argument("a", type=int)
    com_int.add_argument("b", type=int)

    com_choose = add_command(commands, "choose", command_choose)
    com_choose.add_argument("item", nargs="+")


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"randpal {randpal.__version__}",
    )

    register_commands(parser)

    return parser


def cli(args: list[str] | None = None) -> None:
    parser = setup_parser()

    parsed = parser.parse_args(args)
    parsed.command(parsed)
