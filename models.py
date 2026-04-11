from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String)
    group_no = Column(Integer)
    project_name = Column(String)
    project_abstract = Column(String)

# 🔥 Team table
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True)
    password = Column(String)
    year = Column(String)
    mentor_name = Column(String)
    team_code = Column(String, unique=True)
    description = Column(String, nullable=True)
    max_members = Column(Integer, default=4)


# 🔥 Members table
class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    roll_no = Column(String)