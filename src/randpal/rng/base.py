from __future__ import annotations

import operator
from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Protocol,
    SupportsFloat,
    SupportsIndex,
    TypeVar,
    overload,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = [
    "FloatGenerator",
    "IntegerGenerator",
    "RandomProvider",
    "SequencesGenerator",
]


_T = TypeVar("_T")


class RandomProvider(Protocol):
    @abstractmethod
    def randbytes(self, n: int) -> bytes:
        raise NotImplementedError

    # NOTE: It's possible to implement random buffering in future
    def randbits(self, k: int) -> int:
        n = (k + 7) // 8
        value = int.from_bytes(self.randbytes(n), "big")
        return value >> (n * 8 - k)

    def _randbelow(self, n: int) -> int:
        if n <= 0:
            msg = "Empty range -- no values to choose from"
            raise ValueError(msg)

        k = n.bit_length()
        randbits = self.randbits
        r = randbits(k)

        while r >= n:
            r = randbits(k)

        return r


class IntegerGenerator(RandomProvider, Protocol):
    @overload
    def randrange(self, stop: SupportsIndex, /) -> int: ...
    @overload
    def randrange(
        self, start: SupportsIndex, stop: SupportsIndex, /
    ) -> int: ...
    @overload
    def randrange(
        self, start: SupportsIndex, stop: SupportsIndex, step: SupportsIndex, /
    ) -> int: ...

    def randrange(
        self,
        start: SupportsIndex,
        stop: SupportsIndex | None = None,
        step: SupportsIndex = 1,
        /,
    ) -> int:
        try:
            istart = operator.index(start)  # Validate start
        except TypeError as exc:
            tname = type(start).__name__
            msg = f"Arg 1 of type {tname} couldn't be interpreted as integer"
            raise TypeError(msg) from exc

        # Fast path: [0; start)
        if stop is None:
            if step != 1:
                msg = "Step was provided without a non-None stop argument"
                raise TypeError(msg)

            return self._randbelow(istart)

        try:
            istop = operator.index(stop)  # Validate stop
        except TypeError as exc:
            tname = type(stop).__name__
            msg = f"Arg 2 of type {tname} couldn't be interpreted as integer"
            raise TypeError(msg) from exc

        try:
            istep = operator.index(step)  # Validate stop
        except TypeError as exc:
            tname = type(step).__name__
            msg = f"Arg 3 of type {tname} couldn't be interpreted as integer"
            raise TypeError(msg) from exc

        width = istop - istart

        # Fast path: [start; stop)
        if istep == 1:
            return istart + self._randbelow(width)

        if istep == 0:
            msg = "Zero step was provided"
            raise ValueError(msg)

        # Divide width and round in direction from zero
        n = (width + istep + 1 - (istep > 0) * 2) // istep

        return istart + istep * self._randbelow(n)

    def randint(self, a: SupportsIndex, b: SupportsIndex) -> int:
        try:
            ia = operator.index(a)  # Validate a
        except TypeError as exc:
            tname = type(a).__name__
            msg = f"Arg 1 of type {tname} couldn't be interpreted as integer"
            raise TypeError(msg) from exc

        try:
            ib = operator.index(b)  # Validate b
        except TypeError as exc:
            tname = type(b).__name__
            msg = f"Arg 2 of type {tname} couldn't be interpreted as integer"
            raise TypeError(msg) from exc

        width = ib - ia
        return ia + self._randbelow(width + 1)

    def randbool(self) -> bool:
        return bool(self.randbits(1))


class FloatGenerator(RandomProvider, Protocol):
    # These constants use '53' as Python's float is implemented with binary64
    FLOAT_SIGNIFICANT_BITS: ClassVar[int] = 53
    FLOAT_UNIT_INTERVAL_SCALE_FACTOR: ClassVar[int] = 2**FLOAT_SIGNIFICANT_BITS

    def random(self) -> float:
        """Get a random a random number from a unit interval.

        Returns:
            A floating-point value chosen from interval `[0, 1)`.
        """
        return (
            self.randbits(self.FLOAT_SIGNIFICANT_BITS)
            / self.FLOAT_UNIT_INTERVAL_SCALE_FACTOR
        )

    def uniform(self, a: SupportsFloat, b: SupportsFloat) -> float:
        """Get a random floating-point number from the given range.

        Returns:
            A floating-point value chosen from interval `[a, b)`. There
                is a possibility of the number rounding up to `b`.
        """
        try:
            a = float(a)
        except TypeError as exc:
            tname = type(a).__name__
            msg = f"Arg 1 of type {tname} couldn't be interpreted as float"
            raise TypeError(msg) from exc

        try:
            b = float(b)
        except TypeError as exc:
            tname = type(b).__name__
            msg = f"Arg 2 of type {tname} couldn't be interpreted as float"
            raise TypeError(msg) from exc

        width = b - a
        return a + width * self.random()

    def chance(self, probability: SupportsFloat) -> bool:
        """Return `True` with the given probability.

        Args:
            probability: A floating-point probability of returning `True`.
                Must be in a unit interval `[0, 1]`.

        Returns:
            `True` if the random event with a given probability happens,
                and `False` otherwise.
        """
        probability = float(probability)

        if not 0 <= probability <= 1:
            msg = (
                f"Probability {probability} was supplied, being outside "
                "of the allowed interval [0, 1]"
            )
            raise ValueError(msg)

        return self.random() < probability


class SequencesGenerator(RandomProvider, Protocol):
    def choice(self, seq: Sequence[_T]) -> _T:
        return seq[self._randbelow(len(seq))]
