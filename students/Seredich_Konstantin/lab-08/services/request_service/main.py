import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime

import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import RequestRecord, SessionLocal, init_db
from domain.events.request_events import (
    GroupAssignedToRequest,
    RequestActivated,
    RequestCreated,
)
from infrastructure.event_bus.rabbitmq_publisher import RabbitMQPublisher
from infrastructure.http.circuit_breaker import GroupServiceClient


class CreateRequestBody(BaseModel):
    coordinator_id: str
    zone_name: str
    zone_n: float
    zone_s: float
    zone_w: float
    zone_e: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


publisher: RabbitMQPublisher | None = None
group_client: GroupServiceClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global publisher, group_client
    init_db()
    publisher = RabbitMQPublisher(
        host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        username=os.getenv("RABBITMQ_USER", "admin"),
        password=os.getenv("RABBITMQ_PASS", "password"),
    )
    group_client = GroupServiceClient(
        base_url=os.getenv("GROUP_SERVICE_URL", "http://group-service:8000"),
    )
    yield
    if publisher:
        publisher.close()


app = FastAPI(title="Request Service", lifespan=lifespan)


@app.post("/requests")
def create_request(body: CreateRequestBody, db: Session = Depends(get_db)):
    rid = str(uuid.uuid4())
    bounds = (body.zone_n, body.zone_s, body.zone_w, body.zone_e)
    row = RequestRecord(
        id=rid,
        coordinator_id=body.coordinator_id,
        zone_name=body.zone_name,
        status="DRAFT",
        assigned_group_id=None,
    )
    db.add(row)
    db.commit()

    event = RequestCreated(
        event_id=str(uuid.uuid4()),
        occurred_at=datetime.utcnow(),
        request_id=rid,
        coordinator_id=body.coordinator_id,
        zone_name=body.zone_name,
        zone_bounds=bounds,
    )
    publisher.publish(event)

    return {
        "request_id": rid,
        "coordinator_id": body.coordinator_id,
        "zone_name": body.zone_name,
        "status": row.status,
    }


@app.get("/requests/{request_id}")
def get_request(request_id: str, db: Session = Depends(get_db)):
    row = db.get(RequestRecord, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")
    return {
        "request_id": row.id,
        "coordinator_id": row.coordinator_id,
        "zone_name": row.zone_name,
        "status": row.status,
        "assigned_group_id": row.assigned_group_id,
    }


@app.put("/requests/{request_id}/assign-group")
def assign_group(request_id: str, db: Session = Depends(get_db)):
    row = db.get(RequestRecord, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")
    if row.status != "DRAFT":
        raise HTTPException(status_code=400, detail="Can only assign in DRAFT")

    grp = group_client.find_ready_group()
    if not grp:
        raise HTTPException(status_code=503, detail="No ready group available")

    gid = grp["group_id"]
    base = os.getenv("GROUP_SERVICE_URL", "http://group-service:8000")
    try:
        r = requests.put(f"{base}/groups/{gid}/mark-busy", timeout=5)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Group Service: {e}") from e

    row.assigned_group_id = gid
    db.commit()

    publisher.publish(
        GroupAssignedToRequest(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.utcnow(),
            request_id=request_id,
            group_id=gid,
        )
    )

    return {"request_id": request_id, "group_id": gid, "status": row.status}


@app.put("/requests/{request_id}/activate")
def activate(request_id: str, db: Session = Depends(get_db)):
    row = db.get(RequestRecord, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")
    if not row.assigned_group_id:
        raise HTTPException(status_code=400, detail="Assign group first")

    row.status = "ACTIVE"
    db.commit()

    publisher.publish(
        RequestActivated(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.utcnow(),
            request_id=request_id,
            group_id=row.assigned_group_id,
            zone_name=row.zone_name,
        )
    )

    return {
        "request_id": request_id,
        "status": row.status,
        "group_id": row.assigned_group_id,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
