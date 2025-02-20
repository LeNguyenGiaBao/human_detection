import uuid
from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class Record(Base):
    __tablename__ = "detection_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    timestamp = Column(DateTime, default=datetime.now)
    num_boxes = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)
