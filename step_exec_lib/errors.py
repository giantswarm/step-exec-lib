"""Errors returned by step-exec-lib"""
from __future__ import annotations

from typing import List


class Error(Exception):
    """
    Basic error class that just returns a message.
    """

    def __init__(self, message: str):
        super().__init__()
        self.msg = message

    def __str__(self) -> str:
        return self.msg


class ConfigError(Error):
    """
    Error class that shows error in configuration options.
    """

    config_option: str

    def __init__(self, config_option: str, message: str):
        super().__init__(message)
        self.config_option = config_option

    def __str__(self) -> str:
        return f"Error for config option '{self.config_option}': {self.msg}"


class ValidationError(Error):
    """
    ValidationError means some input data (configuration, chart) is impossible to process or fails
    assumptions.
    """

    source: str

    def __init__(self, source: str, message: str):
        super().__init__(message)
        self.source = source

    def __str__(self) -> str:
        return f"Source: '{self.source}', message: {self.msg}."


class AggregatedError(Error):
    """
    Holds multiple errors collected when running with --keep-going. Subclasses Error so
    existing `except Error` catch sites work without modification.
    """

    errors: List[Error]

    def __init__(self, errors: List[Error]):
        super().__init__(f"{len(errors)} errors collected")
        self.errors = errors

    def __str__(self) -> str:
        lines = [f"{len(self.errors)} errors collected:"]
        for i, e in enumerate(self.errors, 1):
            lines.append(f"  {i}. {e}")
        return "\n".join(lines)
