from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# DB connection
conn = sqlite3.connect("bugs.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT
)
""")
conn.commit()

class Bug(BaseModel):
    title: str
    description: str
    status: str = "open"

@app.get("/")
def root():
    return {"message": "Bug Tracker API is running"}

@app.post("/bugs")
def create_bug(bug: Bug):
    cursor.execute(
        "INSERT INTO bugs (title, description, status) VALUES (?, ?, ?)",
        (bug.title, bug.description, bug.status)
    )
    conn.commit()
    return {"message": "Bug added successfully"}

@app.get("/bugs")
def get_bugs():
    cursor.execute("SELECT * FROM bugs")
    rows = cursor.fetchall()
    return rows
