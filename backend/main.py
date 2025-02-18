import base64
import os

import cv2
import numpy as np
from constants import (
    FAILED,
    INPUT_REQUIRED,
    INVALID_FILE,
    MODEL_PATH,
    NOT_FOUND,
    UNAUTHORIZED,
    UPLOAD_DIR,
)
from database import SessionLocal
from database import get_all as get_all_records
from database import get_one as get_one_record
from database import init_db, save_detection
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from model import detect
from response import ResponseFormatter
from sqlalchemy.orm import Session
from ultralytics import YOLO
from utils import gen_filename, utc_to_utc_plus_7

load_dotenv()
os.makedirs(UPLOAD_DIR, exist_ok=True)
SECRET_KEY = os.environ.get("SECRET_KEY", "")
model = YOLO(MODEL_PATH)
init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ResponseFormatter.error(FAILED)


async def get_image_from_request(file):
    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return image
    except Exception:
        return None


@app.post("/upload")
async def upload_file(file: UploadFile = File(None), db: Session = Depends(get_db)):
    try:
        if file is None:
            return ResponseFormatter.error(INPUT_REQUIRED)
        logger.info(f"Received file: {file.filename}")

        image = await get_image_from_request(file)
        if image is None:
            return ResponseFormatter.error(INVALID_FILE)

        result_image, count = detect(model, image)
        result_path = os.path.join(UPLOAD_DIR, gen_filename())
        cv2.imwrite(result_path, result_image)
        save_detection(db, count, result_path)
        _, buffer = cv2.imencode(".jpg", result_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")
        return ResponseFormatter.success({"count": count, "image": base64_image})

    except Exception as e:
        return ResponseFormatter.server_error(str(e))


@app.get("/records")
async def get_records(secret: str, db: Session = Depends(get_db)):
    try:
        if secret != SECRET_KEY:
            return ResponseFormatter.error(UNAUTHORIZED, status_code=401)

        records = get_all_records(db)
        result = [
            {
                "id": str(record.id),
                "timestamp": str(utc_to_utc_plus_7(record.timestamp)),
                "num_boxes": record.num_boxes,
                "image_path": record.image_path,
            }
            for record in records
        ]
        return ResponseFormatter.success(result)
    except Exception as e:
        return ResponseFormatter.server_error(str(e))


@app.get("/records/{id}")
async def get_record(id: str, secret: str, db: Session = Depends(get_db)):
    if secret != SECRET_KEY:
        return ResponseFormatter.error(UNAUTHORIZED, status_code=401)

    record = get_one_record(db, id)
    if not record:
        return ResponseFormatter.error(NOT_FOUND, status_code=404)

    if not os.path.exists(record.image_path):
        return ResponseFormatter.error(NOT_FOUND, status_code=401)

    with open(record.image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    return ResponseFormatter.success(
        {
            "id": str(record.id),
            "timestamp": str(utc_to_utc_plus_7(record.timestamp)),
            "num_boxes": record.num_boxes,
            "image": base64_image,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
