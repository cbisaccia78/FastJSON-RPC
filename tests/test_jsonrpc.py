import pytest
from pydantic import ValidationError

from fastjson_rpc import ErrorObject, JsonRpcRequest, JsonRpcResponse, UNSET


def test_request_is_notification_default_id():
    request = JsonRpcRequest(jsonrpc="2.0", method="ping", params={"foo": "bar"})

    assert request.is_notification() is True
    assert request.id is UNSET


def test_request_is_not_notification_when_id_present():
    request = JsonRpcRequest(jsonrpc="2.0", method="ping", id=1)

    assert request.is_notification() is False


def test_request_rejects_invalid_jsonrpc_version():
    with pytest.raises(ValidationError):
        JsonRpcRequest(jsonrpc="1.0", method="ping")


def test_response_accepts_result_and_flags_non_error():
    response = JsonRpcResponse(jsonrpc="2.0", result={"pong": True}, id=1)

    assert response.is_error() is False
    assert response.error is UNSET


def test_response_accepts_error_and_flags_error():
    response = JsonRpcResponse(
        jsonrpc="2.0",
        error=ErrorObject(code=-32601, message="Method not found"),
        id=1,
    )

    assert response.is_error() is True
    assert response.result is UNSET


def test_response_rejects_both_result_and_error():
    with pytest.raises(ValueError):
        JsonRpcResponse(
            jsonrpc="2.0",
            result="nope",
            error=ErrorObject(code=-32000, message="Custom"),
            id=1,
        )
