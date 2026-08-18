import json
import os
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Basic Python API")

DATA_DIR = Path(os.getenv("NOTES_DIR", "/data"))
NOTES_FILE = DATA_DIR / "notes.json"
DATA_LOCK = Lock()


def load_notes() -> list[str]:
    if not NOTES_FILE.exists():
        return []

    try:
        with NOTES_FILE.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
    except json.JSONDecodeError:
        return []

    if isinstance(data, list) and all(isinstance(note, str) for note in data):
        return data

    return []


def save_notes(notes: list[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with NOTES_FILE.open("w", encoding="utf-8") as file_handle:
        json.dump(notes, file_handle, ensure_ascii=False, indent=2)


notes = load_notes()


@app.get("/")
def root():
    return {"message": "El API está activo"}


@app.get("/add/{note:path}")
def add_note(note: str):
    cleaned_note = note.strip()
    if not cleaned_note:
        raise HTTPException(status_code=400, detail="La nota no puede estar vacía")

    with DATA_LOCK:
        notes.append(cleaned_note)
        save_notes(notes)

    return {"message": "Nota agregada", "note": cleaned_note}


@app.get("/list")
def list_notes():
    return {"notes": notes}
