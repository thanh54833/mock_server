from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()

app.include_router(home_cache_api, prefix="/home_cache_api")

app.mount("/images", StaticFiles(directory="images/avif"), name="images")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
