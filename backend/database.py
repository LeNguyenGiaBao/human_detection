import datetime
import os
import uuid

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Database credentials
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# PostgreSQL connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def create_database():
    connection_url = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    )
    conn = psycopg2.connect(connection_url)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created successfully!")

    cursor.close()
    conn.close()


create_database()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    num_boxes = Column(Integer)
    image_path = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_detection(db, num_boxes: int, visualized_path: str):
    """Save detection result to the database."""
    detection = DetectionResult(num_boxes=num_boxes, image_path=visualized_path)
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


def get_all(db):
    query = db.query(DetectionResult).all()
    return query


def get_one(db, id):
    query = db.query(DetectionResult).filter(DetectionResult.id == id).first()
    return query
