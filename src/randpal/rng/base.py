from __future__ import annotations

import operator
from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, SupportsIndex, TypeVar, overload

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


class FloatGenerator(Protocol):
    def uniform(self, a: float, b: float) -> float:
        raise NotImplementedError

    def chance(self, probability: float) -> bool:
        raise NotImplementedError


class SequencesGenerator(RandomProvider, Protocol):
    def choice(self, seq: Sequence[_T]) -> _T:
        return seq[self._randbelow(len(seq))]
