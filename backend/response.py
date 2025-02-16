from fastapi.responses import JSONResponse
from logger import logger


class ResponseFormatter:
    @staticmethod
    def success(data=None):
        logger.info("Request processed successfully")
        return JSONResponse(
            content={
                "status": 200,
                "message": "success",
                "data": data if data is not None else {},
            },
            status_code=200,
        )

    @staticmethod
    def error(message: str, status_code=400):
        logger.warning(f"Client error: {message}")
        return JSONResponse(
            status_code=status_code,
            content={"status": status_code, "message": "failed", "data": message},
        )

    @staticmethod
    def server_error(exc: Exception):
        logger.error(f"Server error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "failed", "data": str(exc)},
        )
