import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/images/avif", StaticFiles(directory="images/avif"), name="images")

