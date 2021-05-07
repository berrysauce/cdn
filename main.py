import uvicorn
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from loguru import logger
import sys
import os
from pydantic import BaseModel
from typing import Optional
import base64
import random
import string
import json
from PIL import Image
import configparser
from pyfiglet import Figlet
from tools import setup, hashing



'''
        brry CDN
-----------------------------
Self-hosted, easy to use CDN
made in Python 3.9.
License: General Copyright
Author: berrysauce
'''

"""
DONE - Image compression
DONE - Authentication
OPEN - Correct response (change CLI too)
OPEN - Image deletion
OPEN - Fix Uvicorn logger error
"""

setup.start()
app = FastAPI()
security = HTTPBasic()
config = configparser.ConfigParser()
config.read("data/config.ini")
logger.add("data/api.log", format="[{time}] {level} - {message}", level="INFO", rotation="1 week", enqueue=True)
directory = "data"

class Item(BaseModel):
    image: str
    file_type: str
    
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if hashing.verifypw(credentials.password) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        correct_username = secrets.compare_digest(credentials.username, config.get("SERVER", "username"))
        if not correct_username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username
    
@app.get("/")
async def root():
    return {"msg": "BERRYSAUCE CDN - CODE/LICENSE ON GITHUB.COM/BERRYSAUCE/CDN"}

@app.get("/image/{imgID}")
async def get_image(imgID, file_type: str):
    try:
        logger.info("Image request received & completed")
        return FileResponse(directory+"/images/"+imgID+file_type)
    except IOError:
        logger.warning("Requested Image couldn't be found")
        return {"msg": "Error - Image doesn't exist"}

@app.post("/upload")
async def upload(item: Item, username: str = Depends(get_current_username)):
    logger.info(f"Upload request received from user {username}")
    imgID = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))

    # Save Image
    with open(directory+"/images/"+imgID+item.file_type, "wb") as img:
        img.write(base64.b64decode(item.image))
    
    # Compress Image
    img = Image.open(directory+"/images/"+imgID+item.file_type)
    img.save(directory+"/images/"+imgID+item.file_type,optimize=True,quality=80)
    logger.info("Compressed image")
    
    logger.info("Upload request completed")
    return {
        "msg": "Image uploaded",
        "img_id": imgID,
        "img_url": config.get("SERVER", "host")+"/image/"+imgID+"?file_type="+item.file_type
        }
    
@app.delete("/delete/{imgID}")
async def delete(imgID, file_type: str, username: str = Depends(get_current_username)):
    logger.info(f"Delete request received from user {username}")
    try:
        os.remove(directory+"/images/"+imgID+file_type)
        logger.info("Delete request completed")
        return {"msg": "Image deleted sucessfully"}
    except:
        logger.warning("Requested Image couldn't be found")
        return {"msg": "Error - Image doesn't exist"}


logger.info("Starting app")

if __name__ == "__main__":
    uvicorn.run(app, host=str(config.get("SERVER", "host")), port=int(config.get("SERVER", "port")))