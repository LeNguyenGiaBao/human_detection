import base64
import os

import cv2
import numpy as np
from constants import INPUT_REQUIRED, INVALID_FILE, MODEL_PATH
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from model import detect
from response import ResponseFormatter
from ultralytics import YOLO

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ResponseFormatter.error(INVALID_FILE)


async def get_image_from_request(file):
    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return image
    except Exception:
        return None


@app.post("/upload")
async def upload_file(file: UploadFile = File(None)):
    try:
        if file is None:
            return ResponseFormatter.error(INPUT_REQUIRED)

        image = await get_image_from_request(file)
        if image is None:
            return ResponseFormatter.error(INVALID_FILE)

        result_image, count = detect(model, image)
        _, buffer = cv2.imencode(".jpg", result_image)
        base64_image = base64.b64encode(buffer).decode("utf-8")
        return ResponseFormatter.success({"count": count, "image": base64_image})

    except Exception as e:
        return ResponseFormatter.server_error(str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
