from importlib import metadata

from .rng import (
    FloatGenerator,
    IntegerGenerator,
    PythonRandom,
    RandomProvider,
    SecretsRandom,
    SequencesGenerator,
)

__all__ = [
    "FloatGenerator",
    "IntegerGenerator",
    "PythonRandom",
    "RandomProvider",
    "SecretsRandom",
    "SequencesGenerator",
    "__version__",
]
PACKAGE_NAME = "randpal"

try:
    __version__ = metadata.version(PACKAGE_NAME)
except metadata.PackageNotFoundError:
    __version__ = "0.1.dev1+UNKNOWN"
