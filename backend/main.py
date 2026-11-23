from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from transformers import pipeline

from database import Analysis, SessionLocal

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:5173"],
   allow_methods=["*"],
   allow_headers=["*"],
)

# Loaded once when the server starts (not on every request)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)

def get_db():
    db = SessionLocal()
    try:
      yield db
    finally:
      db.close()

class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Hello, the text analyzer is running"}


@app.post("/analyze")
def analyze(data: TextInput, db: Session = Depends(get_db)):
    result = sentiment_model(data.text)[0]
    label = result["label"]
    score = round(result["score"], 4)

    record = Analysis(text=data.text, label=label, score=score)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "text": record.text, "label": record.label, "score": record.score}

@app.get("/history")
def history(db: Session = Depends(get_db)):
   rows = db.query(Analysis).order_by(Analysis.id.desc()).all()
   return[
      {
        "id": r.id,
        "text": r.text,
        "label": r.label,
        "score": r.score,
        "created_at": r.created_at,
      }
      for r in rows
   ]