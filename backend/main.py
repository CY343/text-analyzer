from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Loaded once when the server starts (not on every request)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Hello, the text analyzer is running"}


@app.post("/analyze")
def analyze(data: TextInput):
    result = sentiment_model(data.text)[0]
    return {
        "text": data.text,
        "label": result["label"],
        "score": round(result["score"], 4),
    }