from typing import Any
from pydantic import BaseModel, Field


class UnsetType:
    pass


UNSET = UnsetType()

JsonRpcId = str | int | None


class ErrorObject(BaseModel):
    code: int
    message: str
    data: Any = Field(default=UNSET)

    model_config = {"arbitrary_types_allowed": True}
