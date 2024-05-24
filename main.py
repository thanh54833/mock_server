import json

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import os

app = FastAPI()

# Mount the Swagger UI static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ... (your existing API endpoints)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    openapi_url = "/openapi.json"
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="My API - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    with open(os.path.join("mock_server", "openapi.json"), "r") as f:
        return json.load(f)