from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator

from .helpers import *


class JsonRpcRequest(BaseModel):
    jsonrpc: Literal["2.0"]
    method: str
    params: dict | list[Any] = None
    id: JsonRpcId | UnsetType = Field(default=UNSET)

    def is_notification(self) -> bool:
        return isinstance(self.id, UnsetType)

    model_config = {"arbitrary_types_allowed": True}


class JsonRpcResponse(BaseModel):
    jsonrpc: Literal["2.0"]
    result: Any = Field(default=UNSET)
    error: ErrorObject = Field(default=UNSET)
    id: JsonRpcId

    model_config = {"arbitrary_types_allowed": True}

    # Model validator to ensure either result or error is set, but not both
    @model_validator(mode="after")
    def validate_result_or_error(self):
        has_result = not isinstance(self.result, UnsetType)
        has_error = not isinstance(self.error, UnsetType)

        if has_result == has_error:
            raise ValueError("Response must have either result or error, but not both.")

        return self

    def is_error(self) -> bool:
        return not isinstance(self.error, UnsetType)


r1 = JsonRpcRequest(jsonrpc="2.0", method="subtract", params=[42, 23])

print(r1.is_notification())
