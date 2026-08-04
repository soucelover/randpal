from __future__ import annotations

import secrets

from typing_extensions import override

from .base import IntegerGenerator, RandomProvider


class SecretsRandom(IntegerGenerator, RandomProvider):
    _generator: secrets.SystemRandom

    def __init__(self, generator: secrets.SystemRandom | None = None) -> None:
        if generator is None:
            generator = secrets.SystemRandom()

        self._generator = generator

    @override
    def randbytes(self, n: int) -> bytes:
        return self._generator.randbytes(n)

    @override
    def randbits(self, k: int) -> int:
        return self._generator.getrandbits(k)
