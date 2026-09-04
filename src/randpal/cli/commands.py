from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from randpal.rng import (
        FloatGenerator,
        IntegerGenerator,
        SequencesGenerator,
    )

    from .base import GeneratorCommandArgs, RandomGeneratorFactory


def command_int(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: IntegerGenerator = factory.create_rng(args.provider)
    number = generator.randint(args.a, args.b)

    match args.output_format:
        case "concise":
            print(number)  # noqa: T201
        case "verbose":
            print(f"And so, the random integer is... {number}!", end="\n\n")  # noqa: T201
        case _:
            raise NotImplementedError


def command_float(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: FloatGenerator = factory.create_rng(args.provider)
    number = generator.uniform(args.a, args.b)

    match args.output_format:
        case "concise":
            print(number)  # noqa: T201
        case "verbose":
            print(f"And so, the random number is... {number}!", end="\n\n")  # noqa: T201
        case _:
            raise NotImplementedError


def command_chance(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: FloatGenerator = factory.create_rng(args.provider)

    if not 0 <= args.probability <= 100:  # noqa: PLR2004
        print(  # noqa: T201
            "ERROR: The probability must lie between 0 and 100.",
            file=sys.stderr,
        )
        return

    result = generator.chance(args.probability / 100)

    match args.output_format:
        case "concise":
            print(("no", "yes")[result])  # noqa: T201
        case "verbose":
            if result:
                print('The odds has said "yes"!')  # noqa: T201
            else:
                print("A chance word didn't turn in your favour...")  # noqa: T201
        case "exit-code":
            raise SystemExit(int(not result))
        case _:
            raise NotImplementedError


def command_pick(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: SequencesGenerator = factory.create_rng(args.provider)
    item = generator.choice(args.items)

    match args.output_format:
        case "concise":
            print(item)  # noqa: T201
        case "verbose":
            print(  # noqa: T201
                f'The barrel with cards was shaken and a card with "{item}" '
                "written on it has fallen out.",
                end="\n\n",
            )
        case _:
            raise NotImplementedError
