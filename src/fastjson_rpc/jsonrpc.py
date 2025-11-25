"""Core JSON-RPC request and response models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from .helpers import ErrorObject, JsonRpcId, UNSET, UnsetType


class JsonRpcRequest(BaseModel):
    """Typed representation of a JSON-RPC 2.0 request."""

    jsonrpc: Literal["2.0"]
    method: str
    params: dict[str, Any] | list[Any] | None = None
    id: JsonRpcId | UnsetType = Field(default=UNSET)

    def is_notification(self) -> bool:
        """Return ``True`` when this request omits an ``id``."""

        return isinstance(self.id, UnsetType)

    model_config = {"arbitrary_types_allowed": True}


class JsonRpcResponse(BaseModel):
    """Typed response payload that enforces JSON-RPC invariants."""

    jsonrpc: Literal["2.0"]
    result: Any | UnsetType = Field(default=UNSET)
    error: ErrorObject | UnsetType = Field(default=UNSET)
    id: JsonRpcId

    model_config = {"arbitrary_types_allowed": True}

    # Model validator to ensure either result or error is set, but not both
    @model_validator(mode="after")
    def validate_result_or_error(self) -> "JsonRpcResponse":
        """Ensure callers provide exactly one of ``result`` or ``error``."""

        has_result = not isinstance(self.result, UnsetType)
        has_error = not isinstance(self.error, UnsetType)

        if has_result == has_error:
            raise ValueError("Response must have either result or error, but not both.")

        return self

    def is_error(self) -> bool:
        """Return ``True`` if the response represents an error payload."""

        return not isinstance(self.error, UnsetType)
