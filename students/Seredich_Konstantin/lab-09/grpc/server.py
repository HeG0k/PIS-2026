"""
gRPC Server: Request Service (ПСО «Юго-Запад»)
"""
from __future__ import annotations

import sys
import time
from concurrent import futures
from pathlib import Path

import grpc

_GEN = Path(__file__).resolve().parent.parent / "generated"
sys.path.insert(0, str(_GEN))

import request_service_pb2  # noqa: E402
import request_service_pb2_grpc  # noqa: E402


class RequestServiceServicer(request_service_pb2_grpc.RequestServiceServicer):
    def __init__(self) -> None:
        self.requests: dict[str, request_service_pb2.Request] = {}
        self.counter = 1
        self._seed_data()

    def _seed_data(self) -> None:
        test_requests = [
            ("COORD-1", "North", 52.0, 52.5, 23.5, 24.0, "ACTIVE"),
            ("COORD-2", "South", 51.5, 52.0, 23.5, 24.0, "ACTIVE"),
            ("COORD-3", "East", 52.0, 52.5, 24.0, 24.5, "COMPLETED"),
        ]
        for coord_id, zone_name, lat_min, lat_max, lon_min, lon_max, status in test_requests:
            request_id = f"REQ-2024-{self.counter:04d}"
            zone = request_service_pb2.Zone(
                name=zone_name,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
            )
            req = request_service_pb2.Request(
                request_id=request_id,
                coordinator_id=coord_id,
                zone=zone,
                status=status,
                created_at=int(time.time()) - 3600,
                activated_at=int(time.time()) - 1800 if status == "ACTIVE" else 0,
                completed_at=int(time.time()) if status == "COMPLETED" else 0,
            )
            self.requests[request_id] = req
            self.counter += 1

    def CreateRequest(self, request, context):
        request_id = f"REQ-2024-{self.counter:04d}"
        self.counter += 1
        new_request = request_service_pb2.Request(
            request_id=request_id,
            coordinator_id=request.coordinator_id,
            zone=request.zone,
            status="DRAFT",
            created_at=int(time.time()),
        )
        self.requests[request_id] = new_request
        return request_service_pb2.CreateRequestResponse(
            request_id=request_id,
            status="SUCCESS",
        )

    def GetRequest(self, request, context):
        req = self.requests.get(request.request_id)
        if req:
            return request_service_pb2.GetRequestResponse(request=req, found=True)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f"Request {request.request_id} not found")
        return request_service_pb2.GetRequestResponse(found=False)

    def ListRequests(self, request, context):
        filtered = [
            req
            for req in self.requests.values()
            if not request.status_filter or req.status == request.status_filter
        ]
        limit = request.limit if request.limit > 0 else 100
        results = filtered[:limit]
        return request_service_pb2.ListRequestsResponse(
            requests=results,
            total_count=len(filtered),
        )

    def ActivateRequest(self, request, context):
        req = self.requests.get(request.request_id)
        if not req:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return request_service_pb2.ActivateRequestResponse(
                success=False,
                error_message="Request not found",
            )
        if req.status != "DRAFT":
            return request_service_pb2.ActivateRequestResponse(
                success=False,
                error_message=f"Cannot activate request with status {req.status}",
            )
        req.status = "ACTIVE"
        req.activated_at = int(time.time())
        return request_service_pb2.ActivateRequestResponse(success=True)

    def StreamActiveRequests(self, request, context):
        """Server-side streaming: периодически отдаёт снимок активных заявок."""
        while context.is_active():
            active = [r for r in self.requests.values() if r.status == "ACTIVE"]
            for req in active:
                if not context.is_active():
                    return
                yield req
            time.sleep(1)


def serve(port: int = 50051) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    request_service_pb2_grpc.add_RequestServiceServicer_to_server(
        RequestServiceServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    return server


def main() -> None:
    server = serve()
    print("gRPC RequestService на [::]:50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main()
