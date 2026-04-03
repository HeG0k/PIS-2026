"""Фикстуры: поднятие gRPC-сервера на свободном порту."""
from __future__ import annotations

import importlib.util
import socket
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_server_module():
    path = ROOT / "grpc" / "server.py"
    spec = importlib.util.spec_from_file_location("lab09_request_server", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lab09_request_server"] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="session")
def grpc_port():
    mod = _load_server_module()
    port = _free_port()
    server = mod.serve(port)
    time.sleep(0.3)
    yield port
    server.stop(0)
