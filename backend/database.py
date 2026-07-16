from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# -----------------------------
# Database Connection
# -----------------------------

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:1234@localhost:5434/deeptrust"
)


engine = create_engine(
     DATABASE_URL,
    
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# -----------------------------
# Analysis Table
# -----------------------------

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    result = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)

    audio_file = relationship(
        "AudioFile",
        back_populates="analysis",
        uselist=False
    )


# -----------------------------
# Audio Files Table
# -----------------------------

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Float, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)

    analysis = relationship(
        "Analysis",
        back_populates="audio_file"
    )


# -----------------------------
# Create Tables
# -----------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------
# CRUD - Analysis
# -----------------------------

def save_result(file_name: str, result: str, confidence: float):
    db = SessionLocal()

    try:
        record = Analysis(
            file_name=file_name,
            result=result,
            confidence=confidence
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_all_results():
    db = SessionLocal()

    try:
        return db.query(Analysis).all()

    finally:
        db.close()


def get_result_by_id(id: int):
    db = SessionLocal()

    try:
        return db.query(Analysis).filter(
            Analysis.id == id
        ).first()

    finally:
        db.close()


# -----------------------------
# CRUD - Audio Files
# -----------------------------

def save_audio_file(file_name, file_path, file_size, analysis_id=None):
    db = SessionLocal()

    try:
        record = AudioFile(
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            analysis_id=analysis_id
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_audio_file_by_id(id: int):
    db = SessionLocal()

    try:
        return db.query(AudioFile).filter(
            AudioFile.id == id
        ).first()

    finally:
        db.close()
