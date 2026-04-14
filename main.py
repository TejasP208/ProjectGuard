from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
import sys
import os

# Add the Models directory to Python path if necessary, but we can just import directly if main.py is strictly run from the root.
from Models.search import semantic_search

app = FastAPI(title="ProjectGuard API")

# Allow CORS so the frontend can interact with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect('training_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/projects")
def get_projects():
    """
    Returns a list of all projects from the database.
    """
    conn = get_db_connection()
    projects = conn.execute("SELECT id, year, group_no, project_name, project_abstract FROM projects").fetchall()
    conn.close()
    return [dict(project) for project in projects]

class ProjectCheckRequest(BaseModel):
    title: str
    description: str

@app.post("/api/check_project")
def check_project(request: ProjectCheckRequest):
    """
    Checks if a project already exists using semantic search.
    """
    result = semantic_search(request.title, request.description)
    return {"exists": result["exists"], "best_match": result["best_match"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
