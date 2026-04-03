import os
import threading
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import GroupRecord, MemberRecord, SessionLocal, init_db
from infrastructure.event_bus.rabbitmq_subscriber import RabbitMQSubscriber

MIN_MEMBERS = 3
MAX_MEMBERS = 5


class CreateGroupBody(BaseModel):
    name: str
    leader_id: str


class AddMemberBody(BaseModel):
    volunteer_id: str


class UpdateGroupBody(BaseModel):
    name: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


subscriber: RabbitMQSubscriber | None = None


def run_subscriber():
    global subscriber
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "admin")
    password = os.getenv("RABBITMQ_PASS", "password")

    subscriber = RabbitMQSubscriber(
        host=host,
        port=port,
        username=user,
        password=password,
        queue_name="group_service_queue",
    )

    @subscriber.subscribe("RequestCreated")
    def on_request_created(payload: dict):
        request_id = payload.get("request_id")
        coordinator_id = payload.get("coordinator_id")
        zone_name = payload.get("zone_name")
        print(f"📬 Request created (Group Service): {request_id}")
        print(f"   Coordinator: {coordinator_id}, Zone: {zone_name}")

    try:
        subscriber.start_consuming()
    except KeyboardInterrupt:
        subscriber.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    t = threading.Thread(target=run_subscriber, daemon=True)
    t.start()
    yield


app = FastAPI(title="Group Service", lifespan=lifespan)


def group_to_dict(g: GroupRecord) -> dict:
    return {
        "group_id": g.id,
        "name": g.name,
        "leader_id": g.leader_id,
        "status": g.status,
        "members": [m.volunteer_id for m in g.members],
    }


@app.post("/groups")
def create_group(body: CreateGroupBody, db: Session = Depends(get_db)):
    gid = str(uuid.uuid4())
    row = GroupRecord(id=gid, name=body.name, leader_id=body.leader_id, status="FORMING")
    db.add(row)
    db.commit()
    db.refresh(row)
    return group_to_dict(row)


@app.get("/groups/{group_id}")
def get_group(group_id: str, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    return group_to_dict(g)


@app.delete("/groups/{group_id}")
def delete_group(group_id: str, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status == "BUSY":
        raise HTTPException(status_code=400, detail="Cannot delete BUSY group")
    db.delete(g)
    db.commit()
    return {"deleted": group_id}


@app.get("/groups")
def list_groups(status: str | None = None, db: Session = Depends(get_db)):
    q = select(GroupRecord)
    if status:
        q = q.where(GroupRecord.status == status)
    rows = db.scalars(q).all()
    return [group_to_dict(g) for g in rows]


@app.put("/groups/{group_id}")
def update_group(
    group_id: str,
    body: UpdateGroupBody,
    db: Session = Depends(get_db),
):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status != "FORMING":
        raise HTTPException(status_code=400, detail="Can only edit group in FORMING")
    if body.name is not None:
        g.name = body.name
    db.commit()
    db.refresh(g)
    return group_to_dict(g)


@app.post("/groups/{group_id}/members")
def add_member(group_id: str, body: AddMemberBody, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status != "FORMING":
        raise HTTPException(status_code=400, detail="Cannot change members when not FORMING")
    if len(g.members) >= MAX_MEMBERS:
        raise HTTPException(status_code=400, detail="Too many members")
    if body.volunteer_id in {m.volunteer_id for m in g.members}:
        raise HTTPException(status_code=400, detail="Duplicate member")
    db.add(MemberRecord(group_id=group_id, volunteer_id=body.volunteer_id))
    db.commit()
    db.refresh(g)
    return group_to_dict(g)


@app.delete("/groups/{group_id}/members/{volunteer_id}")
def remove_member(group_id: str, volunteer_id: str, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status != "FORMING":
        raise HTTPException(status_code=400, detail="Cannot change members when not FORMING")
    for m in g.members:
        if m.volunteer_id == volunteer_id:
            db.delete(m)
            db.commit()
            db.refresh(g)
            return group_to_dict(g)
    raise HTTPException(status_code=404, detail="Member not found")


@app.put("/groups/{group_id}/mark-ready")
def mark_ready(group_id: str, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status != "FORMING":
        raise HTTPException(status_code=400, detail="Invalid status for mark-ready")
    if len(g.members) < MIN_MEMBERS:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least {MIN_MEMBERS} members",
        )
    g.status = "READY"
    db.commit()
    db.refresh(g)
    return group_to_dict(g)


@app.put("/groups/{group_id}/mark-busy")
def mark_busy(group_id: str, db: Session = Depends(get_db)):
    g = db.get(GroupRecord, group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.status != "READY":
        raise HTTPException(status_code=400, detail="Group must be READY")
    g.status = "BUSY"
    db.commit()
    db.refresh(g)
    return group_to_dict(g)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
