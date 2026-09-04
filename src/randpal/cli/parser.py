from __future__ import annotations

import inspect
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from typing import TYPE_CHECKING

import randpal

from .base import GeneratorCommandArgs, RandomGeneratorFactory
from .commands import command_int, command_pick

if TYPE_CHECKING:
    from argparse import (
        _SubParsersAction,  # pyright: ignore[reportPrivateUsage]
    )
    from collections.abc import Sequence

    from .base import CommandFunction, GeneratorCommandFunction


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
    help: str | None = None,
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
        help = header

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


def add_generator_command(  # noqa: PLR0913
    commands: _SubParsersAction[ArgumentParser],
    name: str,
    function: GeneratorCommandFunction,
    providers: Sequence[str] = ("python", "secrets"),
    *,
    help: str | None = None,
    epilog: str | None = None,
    aliases: Sequence[str] = (),
) -> ArgumentParser:
    def wrapper(args: GeneratorCommandArgs) -> None:
        factory = RandomGeneratorFactory()

        return function(args, factory)

    parser = add_command(
        commands,
        name,
        wrapper,  # type: ignore [reportArgumentType]
        help=help,
        epilog=epilog,
        aliases=aliases,
    )
    parser.add_argument(
        "--provider",
        default=providers[0],
        choices=providers,
        help="Provider chosen as a source of entropy for random generation.",
    )

    return parser


def register_commands(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)

    com_int = add_generator_command(commands, "int", command_int)
    com_int.add_argument("a", type=int)
    com_int.add_argument("b", type=int)

    com_choose = add_generator_command(commands, "pick", command_pick)
    com_choose.add_argument("items", nargs="+", metavar="item")


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
