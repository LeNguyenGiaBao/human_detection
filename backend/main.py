from app.infrastructure.database import init_db
from app.infrastructure.response import ResponseFormatter
from app.interfaces.controllers import router
from constants import FAILED
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

app = FastAPI()
init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ResponseFormatter.error(FAILED)


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
