import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()
app.include_router(home_cache_api, prefix="/home_cache_api")


def is_running_in_docker():
    return os.path.exists('/.dockerenv')


if is_running_in_docker():
    app.mount("/images/avif", StaticFiles(directory="/app/images/avif"), name="images")
else:
    app.mount("/images/avif", StaticFiles(directory="images/avif"), name="images")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
