"""Biomero schema package."""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("biomero-schema")
except PackageNotFoundError:
    __version__ = "unknown"

from biomero_schema.models import BIOMERO_SCHEMA_VERSION

__all__ = ["__version__", "BIOMERO_SCHEMA_VERSION"]
