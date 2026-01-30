import os
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["bug_tracker_db"]

from fastapi import FastAPI

app = FastAPI(
    title="Bug Tracker API",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def root():
    return {"message": "Bug Tracker API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
