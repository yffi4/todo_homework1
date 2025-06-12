from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base

class NoteCategory(enum.Enum):
    URGENT = "urgent"
    IMPORTANT = "important"
    NORMAL = "normal"
    LOW_PRIORITY = "low_priority"

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category = Column(String)
    ai_category = Column(Enum(NoteCategory), nullable=True)
    ai_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "ai_category": self.ai_category.value if self.ai_category else None,
            "ai_explanation": self.ai_explanation,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")
    notes = relationship("Note", back_populates="owner")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        } 