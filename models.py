from sqlalchemy import Column, Integer, String
from database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    roll1 = Column(String)
    roll2 = Column(String)
    roll3 = Column(String)
    roll4 = Column(String)
    team_name = Column(String)
    year = Column(String)
    mentor_name = Column(String)
    password = Column(String)