from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory word array
words_array: List[str] = []

class Word(BaseModel):
        word: str

@app.get("/words/")
def get_words():
    return {"words": words_array}

@app.post("/words/")
def add_word(word: Word):
    words_array.append(word.word)
    return {"message": "Word added successfully", "words": words_array}

