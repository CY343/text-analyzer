from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
  text: str

@app.get("/")
def home():
  return{"message": "Hello, the text analyzer is running"}

@app.post("/analyze")
def analyze(data: TextInput):
    # Fake result for now. We'll replace this with the real model.
    return {"text": data.text, "label": "POSITIVE", "score": 0.99}
