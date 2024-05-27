import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()


def is_running_in_docker():
    return os.path.exists('/.dockerenv')


if is_running_in_docker():
    app.mount("/images/avif", StaticFiles(directory="/app/images/avif"), name="images")
else:
    app.mount("/images/avif", StaticFiles(directory="images/avif"), name="images")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
