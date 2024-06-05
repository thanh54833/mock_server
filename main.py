import os

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()

app.include_router(home_cache_api, prefix="/home_cache_api")

app.mount("/images", StaticFiles(directory="images/webp"), name="images")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Get a list of all files in the /images directory
    images = os.listdir("images/webp/")

    # Create an HTML page with an <img> tag for each image
    html_content = "<html><body>"
    for image in images:
        html_content += f'<img src="/images/{image}" alt="{image}" style="width: 200px; height: auto;"><br>'
    html_content += "</body></html>"

    return html_content
