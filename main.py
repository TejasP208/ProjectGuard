from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from axiom_ai import Chatbot_stream
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base, Project, Team, TeamMember
from passlib.hash import pbkdf2_sha256
from fastapi import HTTPException
from pydantic import BaseModel
import os
from utils import generate_team_code

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
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

class ProjectSubmission(BaseModel):
    team_name: str
    group_no: int
    project_name: str
    project_abstract: str = ""

class CreateTeamRequest(BaseModel):
    team_name: str
    description: str = ""
    max_members: int = 4

class JoinTeamRequest(BaseModel):
    team_code: str
    roll_no: str

# Endpoints
@app.get("/chat-stream")
def chat_stream(prompt: str):
    return StreamingResponse(Chatbot_stream(prompt), media_type="text/plain")

@app.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()
    try:
        if db.query(Team).filter(Team.team_name == data.team_name).first():
            raise HTTPException(status_code=400, detail="Team name already taken")
        
        hashed_password = pbkdf2_sha256.hash(data.password)
        new_team = Team(
            team_name=data.team_name,
            password=hashed_password,
            year=data.year,
            mentor_name=data.mentor_name
        )
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        
        rolls = [data.roll1, data.roll2, data.roll3, data.roll4]
        for roll in rolls:
            if roll:
                member = TeamMember(team_id=new_team.id, roll_no=roll)
                db.add(member)
        db.commit()
        return {"message": "Signup successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        team = db.query(Team).filter(Team.team_name == data.team_name).first()
        if not team or not pbkdf2_sha256.verify(data.password, team.password):
            raise HTTPException(status_code=401, detail="Invalid team name or password")
        return {
            "message": "Login successful",
            "team_name": team.team_name,
            "year": team.year
        }
    finally:
        db.close()

@app.post("/create-team")
def create_team(data: CreateTeamRequest):
    db = SessionLocal()
    try:
        code = generate_team_code()
        while db.query(Team).filter(Team.team_code == code).first():
            code = generate_team_code()

        new_team = Team(
            team_name=data.team_name,
            team_code=code,
            description=data.description,
            max_members=data.max_members
        )
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return {
            "message": "Team created successfully",
            "team_code": code
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/join-team")
def join_team(data: JoinTeamRequest):
    db = SessionLocal()
    try:
        team = db.query(Team).filter(Team.team_code == data.team_code).first()
        if not team:
            raise HTTPException(status_code=404, detail="Invalid team code")
        
        current_members = db.query(TeamMember).filter(TeamMember.team_id == team.id).count()
        if current_members >= (team.max_members or 4):
            raise HTTPException(status_code=400, detail="Team is full")
        
        new_member = TeamMember(team_id=team.id, roll_no=data.roll_no)
        db.add(new_member)
        db.commit()
        return {"message": "Successfully joined the team"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/submit-project")
def submit_project(data: ProjectSubmission):
    db = SessionLocal()
    try:
        team = db.query(Team).filter(Team.team_name == data.team_name).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        new_project = Project(
            year=team.year,
            group_no=data.group_no,
            project_name=data.project_name,
            project_abstract=data.project_abstract
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return {"message": "Project submitted successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()