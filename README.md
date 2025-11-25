# FastJSON-RPC

Typed utilities for working with JSON-RPC 2.0 messages. FastJSON-RPC ships
strictly-typed Pydantic models for requests and responses, helpers for working
with sentinel values, and human-readable error codes for debugging.

## Features

- JSON-RPC 2.0 request/response models with built-in validation.
- Helper types (`UnsetType`, `JsonRpcId`, `ErrorObject`) re-exported via the
  package root for convenience.
- Boolean helpers (`is_notification`, `is_error`) that express protocol
  semantics.

## Installation

```bash
pip install fastjson-rpc2
```

For local development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Usage

```python
from fastjson_rpc2 import JsonRpcRequest, JsonRpcResponse, ErrorObject

# Build a notification request
request = JsonRpcRequest(jsonrpc="2.0", method="ping", params={"foo": "bar"})

assert request.is_notification()

# Build a response with either result or error
response = JsonRpcResponse(jsonrpc="2.0", result={"pong": True}, id=1)

if response.is_error():
    handle_error(response.error)
else:
    handle_result(response.result)

# Create an error response
error_response = JsonRpcResponse(
    jsonrpc="2.0",
    error=ErrorObject(code=-32601, message="Method not found"),
    id=1,
)

print(error_response.error.human_readable_code()) # -> 'METHOD_NOT_FOUND'
```

## Testing

```bash
pytest
```

## License

MIT
