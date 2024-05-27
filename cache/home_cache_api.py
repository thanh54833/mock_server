import json

from fastapi import APIRouter, Request, Response

home_cache_api = APIRouter()


@home_cache_api.get("/api_1", tags=["home_cache"])
def api_1(request: Request):
    etag = request.headers.get("if-none-match", "")
    print(f"api_1 : {etag} ")

    response = Response(content=json.dumps({"key": "value_2"}))
    response.headers["ETag"] = "W/106384710_1"

    return response
