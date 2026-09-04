from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from randpal.rng import IntegerGenerator, SequencesGenerator

    from .base import GeneratorCommandArgs, RandomGeneratorFactory


VERBOSE_MODE = True


def command_int(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: IntegerGenerator = factory.create_rng(args.provider)
    number = generator.randint(args.a, args.b)

    match args.output_format:
        case "concise":
            print(number)  # noqa: T201
        case "verbose":
            print(f"And so, the random number is... {number}!", end="\n\n")  # noqa: T201
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
