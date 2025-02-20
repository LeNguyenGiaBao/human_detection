from app.domain.models import Record
from sqlalchemy.orm import Session


class RecordService:
    @staticmethod
    def create_record(db: Session, num_boxes: int, image_path: str):
        record = Record(num_boxes=num_boxes, image_path=image_path)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_all_records(db: Session):
        return db.query(Record).all()

    @staticmethod
    def get_record_by_id(db: Session, record_id: str):
        return db.query(Record).filter(Record.id == record_id).first()
