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

    if VERBOSE_MODE:
        print("Random number is ", end="")  # noqa: T201

    print(number, end="\n\n")  # noqa: T201


def command_pick(
    args: GeneratorCommandArgs, factory: RandomGeneratorFactory
) -> None:
    generator: SequencesGenerator = factory.create_rng(args.provider)
    item = generator.choice(args.items)

    if VERBOSE_MODE:
        print("Random chosen item is ", end="")  # noqa: T201

    print(item, end="\n\n")  # noqa: T201
