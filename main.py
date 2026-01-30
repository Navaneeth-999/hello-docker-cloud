import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from passlib.context import CryptContext
from pydantic import BaseModel

# ------------------ MongoDB ------------------
MONGODB_URI = os.getenv("MONGODB_URI")

import certifi

client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where()
)
db = client["bug_tracker_db"]

# ------------------ App ------------------
app = FastAPI(
    title="Bug Tracker API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ------------------ Password Hashing ------------------
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ------------------ Schemas ------------------
class UserCreate(BaseModel):
    email: str
    password: str
# ------------------ Routes ------------------
@app.get("/")
def root():
    return {"message": "Bug Tracker API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup")
def signup(user: UserCreate):
    users_collection = db["users"]

    # check existing user
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)

    users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw
    })

    return {"message": "User created successfully"}
