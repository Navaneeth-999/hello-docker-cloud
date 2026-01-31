from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI(
    title="Bug Tracker API",
    docs_url="/docs"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Bug Tracker API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup")
def signup(user: UserCreate):
    hashed = pwd_context.hash(user.password)
    return {
        "email": user.email,
        "hashed_password": hashed,
        "status": "signup success (DB disabled)"
    }
