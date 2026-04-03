"""Тесты unary RPC и server-side streaming для RequestService."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import grpc
import pytest

ROOT = Path(__file__).resolve().parent.parent
_GEN = ROOT / "generated"
sys.path.insert(0, str(_GEN))

import request_service_pb2  # noqa: E402
import request_service_pb2_grpc  # noqa: E402


def _load_client_helpers():
    path = ROOT / "grpc" / "client.py"
    spec = importlib.util.spec_from_file_location("lab09_request_client", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_create_and_get(grpc_port):
    client_mod = _load_client_helpers()
    addr = f"127.0.0.1:{grpc_port}"
    with grpc.insecure_channel(addr) as ch:
        stub = request_service_pb2_grpc.RequestServiceStub(ch)
        rid = client_mod.create_request(stub, "COORD-TEST")
        assert rid.startswith("REQ-")
        resp = client_mod.get_request(stub, rid)
        assert resp.found
        assert resp.request.status == "DRAFT"


def test_get_not_found(grpc_port):
    addr = f"127.0.0.1:{grpc_port}"
    with grpc.insecure_channel(addr) as ch:
        stub = request_service_pb2_grpc.RequestServiceStub(ch)
        with pytest.raises(grpc.RpcError) as exc:
            stub.GetRequest(
                request_service_pb2.GetRequestRequest(request_id="MISSING-ID")
            )
        assert exc.value.code() == grpc.StatusCode.NOT_FOUND


def test_activate_draft(grpc_port):
    client_mod = _load_client_helpers()
    addr = f"127.0.0.1:{grpc_port}"
    with grpc.insecure_channel(addr) as ch:
        stub = request_service_pb2_grpc.RequestServiceStub(ch)
        rid = client_mod.create_request(stub, "COORD-ACT")
        act = stub.ActivateRequest(
            request_service_pb2.ActivateRequestRequest(request_id=rid)
        )
        assert act.success
        g = client_mod.get_request(stub, rid)
        assert g.request.status == "ACTIVE"


def test_stream_active_requests(grpc_port):
    client_mod = _load_client_helpers()
    addr = f"127.0.0.1:{grpc_port}"
    with grpc.insecure_channel(addr) as ch:
        stub = request_service_pb2_grpc.RequestServiceStub(ch)
        msgs = list(client_mod.stream_active_requests(stub, max_messages=3))
        assert len(msgs) == 3
        for m in msgs:
            assert m.status == "ACTIVE"
