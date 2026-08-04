from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


VERBOSE_MODE = True


def command_int(args: argparse.Namespace) -> None:
    if VERBOSE_MODE:
        print("Random number is ", end="")  # noqa: T201

    print(random.randint(args.a, args.b), end="\n\n")  # noqa: S311, T201


def command_choose(args: argparse.Namespace) -> None:
    if VERBOSE_MODE:
        print("Random chosen item is ", end="")  # noqa: T201

    print(random.choice(args.item), end="\n\n")  # noqa: S311, T201
