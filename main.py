import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/images/avif", StaticFiles(directory="images/avif"), name="images")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)