import argparse
import random

VERBOSE_MODE = True


def command_int(args: argparse.Namespace) -> None:
    if VERBOSE_MODE:
        print("Random number is ", end="")  # noqa: T201

    print(random.randint(args.a, args.b), end="\n\n")  # noqa: T201


def command_choose(args: argparse.Namespace) -> None:
    if VERBOSE_MODE:
        print("Random chosen item is ", end="")  # noqa: T201

    print(random.choice(args.item), end="\n\n")  # noqa: T201


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(required=True)

    com_int = commands.add_parser("int")
    com_int.add_argument("a", type=int)
    com_int.add_argument("b", type=int)
    com_int.set_defaults(command=command_int)

    com_choose = commands.add_parser("choose")
    com_choose.add_argument("item", nargs="+")
    com_choose.set_defaults(command=command_choose)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.command(args)


if __name__ == "__main__":
    main()
