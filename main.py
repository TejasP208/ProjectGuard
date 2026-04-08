from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from axiom_ai import Chatbot_stream
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from database import SessionLocal
from models import Team
from passlib.hash import pbkdf2_sha256
from fastapi import HTTPException
from pydantic import BaseModel
import os


print("DB PATH:", os.path.abspath("projectguard.db"))


Base.metadata.create_all(bind=engine)


class SignupRequest(BaseModel):
    roll1: str
    roll2: str
    roll3: str
    roll4: str
    team_name: str
    year: str
    mentor_name: str
    password: str


class LoginRequest(BaseModel):
    team_name: str
    password: str


app = FastAPI()

# Streaming response
@app.get("/chat-stream")
def chat_stream(prompt: str):
    return StreamingResponse(Chatbot_stream(prompt), media_type="text/plain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Signup endpoint
@app.post("/signup")
def signup(request: SignupRequest):
    db = SessionLocal()

    print("Incoming signup data:", request.dict())  # 🔥 DEBUG

    hashed_password = pbkdf2_sha256.hash(request.password)

    new_team = Team(
        roll1=request.roll1,
        roll2=request.roll2,
        roll3=request.roll3,
        roll4=request.roll4,
        team_name=request.team_name,
        year=request.year,
        mentor_name=request.mentor_name,
        password=hashed_password
    )

    db.add(new_team)
    db.commit()

    print("Saved user:", new_team.team_name)  

    db.close()

    return {"message": "Account created successfully"}

@app.post("/login") 
def login(request: LoginRequest):
    db = SessionLocal()

    team = db.query(Team).filter(
        Team.team_name == request.team_name
    ).first()

    db.close()

    if not team:
        raise HTTPException(status_code=401, detail="User not found")

    if not pbkdf2_sha256.verify(request.password, team.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful"}
