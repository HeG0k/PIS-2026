"""
gRPC Client: Request Service (ПСО «Юго-Запад»)
"""
from __future__ import annotations

import sys
from pathlib import Path

import grpc

_GEN = Path(__file__).resolve().parent.parent / "generated"
sys.path.insert(0, str(_GEN))

import request_service_pb2  # noqa: E402
import request_service_pb2_grpc  # noqa: E402


def create_request(stub: request_service_pb2_grpc.RequestServiceStub, host_coord: str = "COORD-1"):
    zone = request_service_pb2.Zone(
        name="North",
        lat_min=52.0,
        lat_max=52.5,
        lon_min=23.5,
        lon_max=24.0,
    )
    req = request_service_pb2.CreateRequestRequest(
        coordinator_id=host_coord,
        zone=zone,
    )
    response = stub.CreateRequest(req)
    if response.status == "SUCCESS":
        return response.request_id
    raise RuntimeError(response.error_message or "CreateRequest failed")


def get_request(stub, request_id: str) -> request_service_pb2.GetRequestResponse:
    return stub.GetRequest(
        request_service_pb2.GetRequestRequest(request_id=request_id)
    )


def stream_active_requests(stub, max_messages: int | None = None):
    """Итерирует server-side stream. Если max_messages задан — останавливается после N сообщений."""
    req = request_service_pb2.StreamActiveRequestsRequest()
    stream = stub.StreamActiveRequests(req)
    count = 0
    for msg in stream:
        yield msg
        count += 1
        if max_messages is not None and count >= max_messages:
            break


def run_demo(address: str = "localhost:50051") -> None:
    with grpc.insecure_channel(address) as channel:
        stub = request_service_pb2_grpc.RequestServiceStub(channel)
        rid = create_request(stub)
        print(f"Создана заявка: {rid}")
        g = get_request(stub, rid)
        print(f"Чтение: found={g.found}, status={g.request.status if g.found else '—'}")
        act = stub.ActivateRequest(
            request_service_pb2.ActivateRequestRequest(request_id=rid)
        )
        print(f"Активация: success={act.success}")
        print("Первые 5 сообщений StreamActiveRequests:")
        for i, r in enumerate(stream_active_requests(stub, max_messages=5)):
            print(f"  {i + 1}. {r.request_id} {r.status} {r.zone.name}")


if __name__ == "__main__":
    run_demo()
