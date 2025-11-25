"""fastjson-rpc public API."""

from importlib import metadata as _metadata

from .helpers import ErrorObject, JsonRpcId, UNSET, UnsetType
from .jsonrpc import JsonRpcRequest, JsonRpcResponse

__all__ = [
    "JsonRpcRequest",
    "JsonRpcResponse",
    "JsonRpcId",
    "ErrorObject",
    "UNSET",
    "UnsetType",
    "__version__",
]

try:
    __version__ = _metadata.version("fastjson_rpc")
except _metadata.PackageNotFoundError:  # pragma: no cover - fallback for local dev
    __version__ = "0.0.0"
