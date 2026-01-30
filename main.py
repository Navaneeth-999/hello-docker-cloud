import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext

# ---------------- CONFIG ----------------

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set")

client = MongoClient(MONGODB_URI)
db = client["bug_tracker_db"]
users_collection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- APP ----------------

app = FastAPI(
    title="Bug Tracker API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------- MODELS ----------------

class UserCreate(BaseModel):
    email: str
    password: str

# ---------------- UTILS ----------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ---------------- ROUTES ----------------

@app.get("/")
def root():
    return {"message": "Bug Tracker API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup")
def signup(user: UserCreate):
    try:
        # check if user already exists
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(user.password)

        users_collection.insert_one({
            "email": user.email,
            "password": hashed_password
        })

        return {"message": "User created successfully"}

    except HTTPException:
        raise

    except Exception as e:
        print("SIGNUP ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
