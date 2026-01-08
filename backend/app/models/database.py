from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Game(Base):
    """Database model for analyzed games"""
    __tablename__ = "games"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Video info
    filename = Column(String)
    video_path = Column(String)
    duration = Column(Float)
    fps = Column(Float)
    resolution = Column(String)

    # Game result
    winner = Column(String, nullable=True)
    player_playstyle = Column(String)

    # Decks (JSON)
    player_deck = Column(JSON)
    opponent_deck = Column(JSON)

    # Analysis data (JSON)
    moves = Column(JSON)
    move_evaluations = Column(JSON)
    win_probability_timeline = Column(JSON)
    key_moments = Column(JSON)
    statistics = Column(JSON)
    recommendations = Column(JSON)

    # Status
    analysis_status = Column(String, default="completed")


# Create tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
