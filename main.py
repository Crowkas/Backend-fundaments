from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app2 = FastAPI()

@app2.get("/url")
def get_url(url: str):
    response = requests.get(url)
    response_list = response.json()
    return JSONResponse(status_code = 200, content = jsonable_encoder(response_list))