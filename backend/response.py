from fastapi.responses import JSONResponse


class ResponseFormatter:
    @staticmethod
    def success(data=None):
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
        return JSONResponse(
            status_code=400,
            content={"status": 400, "message": "failed", "data": message},
        )

    @staticmethod
    def server_error(exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "failed", "data": str(exc)},
        )
