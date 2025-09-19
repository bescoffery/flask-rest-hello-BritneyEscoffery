from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False) 
    password = Column(String(120), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    events_organized = relationship('Event', backref = "event_post", lazy = True)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Event(db.Model):
    id = Column(Integer, primary_key = True)
    name = Column(String(120), unique = False, nullable = False)
    time = Column(DateTime, default = datetime.now(timezone.utc), unique = False, nullable = False)
    event_planner = Column(Integer, ForeignKey("user.id"), nullable = False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "time": self.time,
            "event_planner": self.event_planner
        }