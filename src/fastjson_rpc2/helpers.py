"""Helper types and utilities shared across the public API."""

from typing import Any
from enum import Enum

from pydantic import BaseModel, Field


class UnsetType:
    """Sentinel used to differentiate omitted values from explicit ``None``."""


UNSET = UnsetType()

JsonRpcId = str | int | None


class ErrorCode(Enum):
    """Named constants for the JSON-RPC 2.0 standard error codes."""

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


class ErrorObject(BaseModel):
    """Concrete error payload adhering to the JSON-RPC specification."""

    code: int
    message: str
    data: Any = Field(default=UNSET)

    model_config = {"arbitrary_types_allowed": True}

    def human_readable_code(self) -> str:
        """Return an enum-style label for known codes to aid logging."""

        try:
            return ErrorCode(self.code).name
        except ValueError:
            if self.code >= -32099 and self.code <= -32000:
                return "SERVER_ERROR_CODE"
            return "UNKNOWN_ERROR_CODE"
