from app.infrastructure.database import init_db
from app.interfaces.controllers import router
from fastapi import FastAPI

app = FastAPI()
init_db()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
