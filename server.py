import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from loguru import logger
import sys
from pydantic import BaseModel
from typing import Optional
import base64
import random
import string
import json

app = FastAPI()
logger.add("api.log", format="[{time}] {level} - {message}", level="INFO", rotation="1 week", enqueue=True)

class Item(BaseModel):
    image: str
    
@app.get("/")
async def root():
    return {"msg": "BERRYSAUCE API - CODE/LICENSE ON GITHUB.COM/BERRYSAUCE/CDN"}

@app.get("/image/{imgID}")
async def get_image(imgID):
    logger.info("Image request received & completed")
    return FileResponse("images/"+imgID+".png")

@app.post("/upload")
async def upload(item: Item):
    logger.info("Upload request received")
    imgID = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))

    with open("images/"+imgID+".png", "wb") as img:
        img.write(base64.b64decode(item.image))
    
    logger.info("Upload request completed")
    return imgID

if __name__ == "__main__":
    logger.info("Starting app")
    uvicorn.run(app, host="127.0.0.1", port=8000)