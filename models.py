import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class SessionModel(Base):
    __tablename__ = 'sessions'
    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    emotions = relationship("EmotionModel", back_populates="session")

class EmotionModel(Base):
    __tablename__ = 'emotions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey('sessions.session_id'))
    emotion = Column(String)
    timestamp = Column(DateTime)
    session = relationship("SessionModel", back_populates="emotions")