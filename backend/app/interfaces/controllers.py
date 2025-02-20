import base64
import os

import cv2
import numpy as np
from app.application.services import RecordService
from app.infrastructure.database import get_db
from app.infrastructure.response import ResponseFormatter
from app.infrastructure.utils import gen_filename
from constants import INPUT_REQUIRED, INVALID_FILE, NOT_FOUND, UNAUTHORIZED, UPLOAD_DIR
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, UploadFile
from model import detect
from sqlalchemy.orm import Session

router = APIRouter()
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "")


@router.post("/record")
async def create_record(file: UploadFile = File(None), db: Session = Depends(get_db)):
    if file is None:
        return ResponseFormatter.error(INPUT_REQUIRED)
    try:
        image_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return ResponseFormatter.error(INVALID_FILE)

        result_image, count = detect(image)
        result_path = os.path.join(UPLOAD_DIR, gen_filename())
        cv2.imwrite(result_path, result_image)

        record = RecordService.create_record(db, count, result_path)
        _, buffer = cv2.imencode(".jpg", result_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")

        return ResponseFormatter.success(
            {"id": str(record.id), "count": count, "image": base64_image}
        )
    except Exception as e:
        return ResponseFormatter.server_error(e)


@router.get("/record")
def get_all_records(secret: str, db: Session = Depends(get_db)):
    if secret != SECRET_KEY:
        return ResponseFormatter.error(UNAUTHORIZED, status_code=401)
    try:
        records = RecordService.get_all_records(db)
        result = [
            {
                "id": str(record.id),
                "timestamp": str(record.timestamp),
                "num_boxes": record.num_boxes,
                "image_path": record.image_path,
            }
            for record in records
        ]
        return ResponseFormatter.success(result)

    except Exception as e:
        return ResponseFormatter.server_error(str(e))


@router.get("/record/{record_id}")
def get_record(record_id: str, secret: str, db: Session = Depends(get_db)):
    if secret != SECRET_KEY:
        return ResponseFormatter.error(UNAUTHORIZED, status_code=401)
    try:
        record = RecordService.get_record_by_id(db, record_id)
        if not record:
            return ResponseFormatter.error(NOT_FOUND, status_code=404)

        with open(record.image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        return ResponseFormatter.success(
            {
                "id": str(record.id),
                "timestamp": str(record.timestamp),
                "num_boxes": record.num_boxes,
                "image": base64_image,
            }
        )
    except Exception as e:
        return ResponseFormatter.server_error(str(e))
