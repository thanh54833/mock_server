import subprocess

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()

app.include_router(home_cache_api, prefix="/home_cache_api")

app.mount("/images", StaticFiles(directory="images/avif"), name="images")

@app.on_event("startup")
def startup_event():
    #print("Starting up...")
    #subprocess.run(["python", "add_tag_openapi.py"], check=True)
    #subprocess.run(["python", "png_to_avif.py"], check=True)
    #subprocess.run(["python", "download_image.py"], check=True)

    print("Starting up...")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
