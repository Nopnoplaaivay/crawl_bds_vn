import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.common.consts import CommonConsts
from src.views import overview, city

app = FastAPI()

# Mount static and templates directories
app.mount("/static", StaticFiles(directory=CommonConsts.STATIC_PATH), name="static")

app.include_router(overview.router)
app.include_router(city.router)

if __name__ == "__main__":
    uvicorn.run(app)