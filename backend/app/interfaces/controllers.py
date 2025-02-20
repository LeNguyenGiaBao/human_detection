import base64
import os

import cv2
import numpy as np
from app.application.services import RecordService
from app.infrastructure.database import get_db
from app.infrastructure.utils import gen_filename
from constants import UPLOAD_DIR
from fastapi import APIRouter, Depends, File, UploadFile
from model import detect
from response import ResponseFormatter
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/record")
async def create_record(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        image_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return ResponseFormatter.error("Invalid image file")

        result_image, count = detect(image)
        result_path = os.path.join(UPLOAD_DIR, gen_filename())
        cv2.imwrite(result_path, result_image)

        record = RecordService.create_record(db, count, result_path)
        _, buffer = cv2.imencode(".jpg", result_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")

        return ResponseFormatter.success(
            {"id": record.id, "count": count, "image": base64_image}
        )
    except Exception as e:
        return ResponseFormatter.server_error(e)


@router.get("/record")
def get_all_records(db: Session = Depends(get_db)):
    records = RecordService.get_all_records(db)
    return ResponseFormatter.success(records)


@router.get("/record/{record_id}")
def get_record(record_id: str, db: Session = Depends(get_db)):
    record = RecordService.get_record_by_id(db, record_id)
    if not record:
        return ResponseFormatter.error("Record not found", status_code=404)

    with open(record.image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    return ResponseFormatter.success(
        {"id": record.id, "count": record.num_boxes, "image": base64_image}
    )
