from datetime import datetime

from app.infrastructure.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    num_boxes = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)
