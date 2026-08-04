from __future__ import annotations

import random

from typing_extensions import override

from .base import IntegerGenerator, RandomProvider


class PythonRandom(IntegerGenerator, RandomProvider):
    _generator: random.Random

    def __init__(self, generator: random.Random | None = None) -> None:
        if generator is None:
            generator = random.Random()  # noqa: S311

        self._generator = generator

    @override
    def randbytes(self, n: int) -> bytes:
        return self._generator.randbytes(n)

    @override
    def randbits(self, k: int) -> int:
        return self._generator.getrandbits(k)
