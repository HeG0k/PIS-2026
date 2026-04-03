from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infrastructure.config.database import SessionLocal
from infrastructure.adapter.out_bound.deck_repository import DeckRepositoryImpl, DeckOrmModel
import uuid

app = FastAPI(title="Говорю Красиво API", version="1.0")

# --- Dependency Injection для БД сессии ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- DTO для API (Pydantic модели) ---
class CreateDeckRequest(BaseModel):
    title: str
    owner_id: str

# --- Эндпоинты (API) ---
@app.post("/decks/", status_code=201)
def create_deck(request: CreateDeckRequest, db: Session = Depends(get_db)):
    repo = DeckRepositoryImpl(db)
    
    # В реальном проекте здесь бы вызывался Command Handler из Лабы 4
    # Для простоты, логика здесь:
    deck_id = str(uuid.uuid4())
    # deck = Deck(deck_id=deck_id, title=request.title, owner_id=request.owner_id, ...)
    
    # Имитация
    fake_domain_deck = type('Deck', (object,), {
        'id': deck_id, 
        '_title': request.title, 
        '_owner_id': request.owner_id
    })()
    
    repo.save(fake_domain_deck)
    return {"id": deck_id, "title": request.title}

@app.get("/decks/{deck_id}")
def get_deck_by_id(deck_id: str, db: Session = Depends(get_db)):
    repo = DeckRepositoryImpl(db)
    deck = repo.get_by_id(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Колода не найдена")
    return deck

@app.get("/health")
def health_check():
    return {"status": "OK"}