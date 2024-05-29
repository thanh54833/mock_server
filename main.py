import subprocess

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()

app.include_router(home_cache_api, prefix="/home_cache_api")

app.mount("/images", StaticFiles(directory="images/avif"), name="images")


@app.on_event("startup")
def startup_event():
    # print("Starting up...")
    # subprocess.run(["python", "add_tag_openapi.py"], check=True)
    # subprocess.run(["python", "png_to_avif.py"], check=True)
    # subprocess.run(["python", "download_image.py"], check=True)

    # # Add all changes to the staging area
    # subprocess.run(["git", "add", "--all"], check=True)
    # # Commit the changes with a message
    # subprocess.run(["git", "commit", "-m", "+ auto push code"], check=True)
    # # Push the changes to the 'main' branch on the 'origin' remote
    # subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)

    print("Starting up...")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
