from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Sequence

_T = TypeVar("_T")


class RandomProvider(Protocol):
    @abstractmethod
    def randbytes(self, n: int) -> bytes:
        raise NotImplementedError

    def randbits(self, k: int) -> int:
        n = (k + 7) // 8
        value = int.from_bytes(self.randbytes(n), "big")
        return value >> (n * 8 - k)


class IntegerGenerator(Protocol):
    @overload
    def randrange(self, stop: int, /) -> int: ...
    @overload
    def randrange(self, start: int, stop: int, /) -> int: ...
    @overload
    def randrange(self, start: int, stop: int, step: int, /) -> int: ...

    def randrange(
        self, start: int, stop: int | None = None, step: int = 1, /
    ) -> int:
        raise NotImplementedError

    def randint(self, a: int, b: int) -> int:
        return self.randrange(a, b + 1)

    def randbool(self) -> bool:
        return bool(self.randrange(2))


class FloatGenerator(Protocol):
    def uniform(self, a: float, b: float) -> float:
        raise NotImplementedError

    def chance(self, probability: float) -> bool:
        raise NotImplementedError


class SequencesGenerator(Protocol):
    def choice(self, seq: Sequence[_T]) -> _T:
        raise NotImplementedError
