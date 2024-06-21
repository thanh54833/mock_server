import os
import subprocess
from urllib.parse import quote

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from cache.home_cache_api import home_cache_api

app = FastAPI()

app.include_router(home_cache_api, prefix="/home_cache_api")
app.mount("/images", StaticFiles(directory="images/webp"), name="images")
# app.mount("/videos", StaticFiles(directory="videos"), name="videos")

@app.get("/.well-known/assetlinks.json")
async def get_assetlinks():
    assetLinks = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.concung.ec.uat",
                "sha256_cert_fingerprints": ["E3:E0:80:6A:4D:7B:3E:87:D9:EA:FA:4F:D8:A1:F6:BB:98:2C:3F:87:55:0E:24:AA:62:49:42:75:63:4C:69:78"]
            }
        }
    ]
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
    # redir = "https%3A%2F%2Fshopee.vn%2Fproduct%2F286157142%2F9212069606%3Fd_id%3D9dea6%26smtt%3D0.117835879-1666671971.9%26utm_campaign%3D-%26utm_content%3Dproduct%26utm_medium%3Daffiliates%26utm_source%3Dan_17358790000%26utm_term%3Dbb3hzmv56y4k#home?navRoute=eyJwYXRocyI6W3sicm5OYXYiOnsidXJsIjoiaHR0cHM6Ly9zaG9wZWUudm4vcHJvZHVjdC8yODYxNTcxNDIvOTIxMjA2OTYwNj9hbnJfaW1wcm92PXRydWUmZF9pZD05ZGVhNiZzbXR0PTAuMTE3ODM1ODc5LTE2NjY2NzE5NzEuOSZ1dG1fY2FtcGFpZ249LSZ1dG1fY29udGVudD1wcm9kdWN0JnV0bV9tZWRpdW09YWZmaWxpYXRlcyZ1dG1fc291cmNlPWFuXzE3MzU4NzkwMDAwJnV0bV90ZXJtPWJiM2h6bXY1Nnk0ayJ9fSx7IndlYk5hdiI6eyJ1cmwiOiJodHRwczovL3Nob3BlZS52bi9wcm9kdWN0LzI4NjE1NzE0Mi85MjEyMDY5NjA2P2Fucl9pbXByb3Y9dHJ1ZSZkX2lkPTlkZWE2JnNtdHQ9MC4xMTc4MzU4NzktMTY2NjY3MTk3MS45JnV0bV9jYW1wYWlnbj0tJnV0bV9jb250ZW50PXByb2R1Y3QmdXRtX21lZGl1bT1hZmZpbGlhdGVzJnV0bV9zb3VyY2U9YW5fMTczNTg3OTAwMDAmdXRtX3Rlcm09YmIzaHptdjU2eTRrIn19XX0%3D&anr_improv=true&d_id=9dea6&smtt=0.117835879-1666671971.9&utm_campaign=-&utm_content=product&utm_medium=affiliates&utm_source=an_17358790000&utm_term=bb3hzmv56y4k"
    # return RedirectResponse(url=f"https://shopee.vn/app?redir={redir}")

    redir = "https://concung.com/bim-ta-khuyen-mai/ta-quan-molflix-size-l-68-mieng-9-13kg-59060.html"
    encoded_redir = quote(redir, safe='')

    return RedirectResponse(url="http://10.10.11.159:8002/app?redir=" + encoded_redir)


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
