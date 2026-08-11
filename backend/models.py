from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    research_id = Column(String, unique=True, index=True) # Pseudonymized ID, e.g., P001
    consent_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="participant")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    session_date = Column(DateTime, default=datetime.utcnow)
    
    participant = relationship("Participant", back_populates="sessions")
    trials = relationship("Trial", back_populates="session")

class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question_id = Column(String)
    
    # Paths to raw files or storage URLs
    audio_file_path = Column(String, nullable=True)
    video_file_path = Column(String, nullable=True)
    physiological_file_path = Column(String, nullable=True)

    # ML results
    prediction_truthful_prob = Column(Float, nullable=True)
    prediction_confidence = Column(Float, nullable=True)
    fusion_method = Column(String, nullable=True)
    
    session = relationship("Session", back_populates="trials")
