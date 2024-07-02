import os
import subprocess
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from urllib.parse import quote

from cache.home_cache_api import home_cache_api


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if "/images/" in request.url.path:
            response.headers['ETag'] = 'cc7ca07af4aca4e0e1be5124fb4f1420'
            response.headers['Cache-Control'] = 'public, max-age=3600'
        return response


app = FastAPI()
app.add_middleware(CustomHeaderMiddleware)

app.include_router(home_cache_api, prefix="/home_cache_api")
app.mount("/images", StaticFiles(directory="images/webp"), name="images")

# ETag: "cc7ca07af4aca4e0e1be5124fb4f1420" , Cache-Control : public, max-age=3600
app.mount("/videos", StaticFiles(directory="videos/mp4"), name="videos")


@app.get("/.well-known/assetlinks.json")
async def get_assetlinks():
    assetLinks = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.concung.ec.uat",
                "sha256_cert_fingerprints": [
                    "E3:E0:80:6A:4D:7B:3E:87:D9:EA:FA:4F:D8:A1:F6:BB:98:2C:3F:87:55:0E:24:AA:62:49:42:75:63:4C:69:78"]
            }
        }
    ]
    return JSONResponse(content=assetLinks)


@app.get("/.well-known/apple-app-site-association")
async def get_assetlinks():
    assetLinks = {
        "applinks": {
            "apps": [],
            "details": [
                {
                    "appIDs": [
                        "6T4TC4WZGU.com.concung.ec.uat"
                    ],
                    "paths": [
                        "*"
                    ],
                    "components": [
                        {
                            "/": "/*"
                        }
                    ]
                }
            ]
        },
        "webcredentials": {
            "apps": [
                "6T4TC4WZGU.com.concung.ec.uat"
            ]
        },
        "appclips": {
            "apps": []
        }
    }

    return JSONResponse(content=assetLinks)


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


@app.get("/progressive_image", response_class=HTMLResponse)
async def progressive_image():
    # Define the command as a string
    command = ""

    # Use subprocess.run() to execute the command
    process = subprocess.run("python3 download_image.py", shell=True, check=True, text=True, capture_output=True)
    git_process = subprocess.run(
        "git add images/ && git commit -m \"+ progressive_image: jenkin push code.\" && git push origin HEAD:main",
        shell=True, check=True,
        text=True, capture_output=True)

    return process.stdout + "\n" + git_process.stdout


@app.get("/short/123")
async def short(request: Request):
    redir = "https://concung.com/bim-ta-khuyen-mai/ta-quan-molflix-size-l-68-mieng-9-13kg-59060.html"
    encoded_redir = quote(redir, safe='')

    return RedirectResponse(url="http://10.10.11.89:8002/app?redir=" + encoded_redir)


@app.get("/short/124")
async def short(request: Request):
    redir = "https://beta.concung.vn/tim-kiem?attr=8_5220&manufac=811&have_reduce_price=1&s=1&p=1&q=s%E1%BB%AFa"
    encoded_redir = quote(redir, safe='')

    return RedirectResponse(url="http://10.10.11.89:8002/app?redir=" + encoded_redir)


@app.get("/short/125")
async def short(request: Request):
    redir = "https://beta.concung.vn/tim-kiem?attr=8_5220&manufac=811&have_reduce_price=1&s=1&p=1&q=s%E1%BB%AFa"
    encoded_redir = quote(redir, safe='')

    return RedirectResponse(url="https://fastapi-simple-43fff848e5df.herokuapp.com/app?redir=" + encoded_redir)


# <data android:scheme="http" android:host="10.10.11.169" android:pathPrefix="/app" />
@app.get("/app")
async def dynamic_link(redir: str, request: Request):
    user_agent = request.headers.get('user-agent')

    if 'android' in user_agent.lower():
        store_url = "https://play.google.com/store/apps/details?id=com.concung.ecapp"
    elif 'iphone' in user_agent.lower():
        store_url = "https://apps.apple.com/app/1442035575"
    else:
        store_url = "https://concung.com/"

    return HTMLResponse(
        f"""
       <html>
    <body>
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">
        <button style="margin: 10px; height: 15vh; width: 40vh; padding: 40px; font-size: 50px;" onclick="window.location.href='{store_url}'">Open App</button>
        <button style="margin: 10px; height: 15vh; width: 40vh; padding: 40px; font-size: 50px;" onclick="window.location.href='{store_url}'">Install App</button>
    </div>
    
    
    <script>
        setTimeout(function() {{
            window.location.href = "{redir}";
        }}, 5000);
     </script>
    
    </body>
    </html>
        """
    )
