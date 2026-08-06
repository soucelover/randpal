from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable
from typing import Literal, TypeAlias

from randpal.rng import PythonRandom, SecretsRandom

CommandFunction: TypeAlias = Callable[[Namespace], None]
GeneratorCommandFunction: TypeAlias = Callable[
    ["GeneratorCommandArgs", "RandomGeneratorFactory"], None
]
ProviderCode: TypeAlias = Literal["python", "secrets"]


class RandomGeneratorFactory:
    def create_python_rng(self) -> PythonRandom:
        return PythonRandom()

    def create_secrets_rng(self) -> SecretsRandom:
        return SecretsRandom()

    def create_rng(self, code: ProviderCode) -> PythonRandom | SecretsRandom:
        match code:
            case "python":
                return self.create_python_rng()
            case "secrets":
                return self.create_secrets_rng()


class GeneratorCommandArgs(Namespace):
    provider: ProviderCode
