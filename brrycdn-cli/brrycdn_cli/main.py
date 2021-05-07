import typer
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

app = typer.Typer()

@app.command()
def upload(host: str, username: str, password: str):
    typer.echo("Choose an image to upload")
    Tk().withdraw()
    image_path = askopenfilename()
    root, extension = os.path.splitext(image_path)
    typer.secho("Uploading image...", fg=typer.colors.BRIGHT_BLUE)
    
    try:
        with open(image_path, "rb") as image_file:
            image = base64.b64encode(image_file.read())
        data = json.dumps({"image":image.decode("utf-8"),
                           "file_type": extension})
        r = requests.post(host+"/upload", data=data, auth = HTTPBasicAuth(username, password))
    except:
        typer.secho("Error - failed to convert/upload image", fg=typer.colors.RED)
        return
    if r.status_code == 200:
        data = json.loads(r.text)
        url = data["img_url"]
        typer.secho(f"Image uploaded - Link: http://{url}", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Error - got response {r.status_code}", fg=typer.colors.RED)


@app.command()
def delete(image_id: str, file_type: str, host: str, username: str, password: str):
    typer.echo(f"Connecting to server...")

    try:
        r = requests.post(host+"/delete/"+image_id+"?file_type="+file_type, auth = HTTPBasicAuth(username, password))
        data = json.loads(r.text)
        msg = data["msg"]
        typer.secho(f"Got {r.status_code} - {msg}", fg=typer.colors.GREEN)
    except:
        typer.secho(f"Error - got response {r.status_code}", fg=typer.colors.RED)