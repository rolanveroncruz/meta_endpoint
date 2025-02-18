from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/api/")
async def root():

    return {"whoami":"rolanvc.dev"}


@app.get("/api/meta_webhook")
async def meta_webhook():
    """ This is the main endpoint for VERIFICATION REQUEST.
    Actually, it may also be the same endpoint for EVENT NOTIFICATION"""

    return {"message": "Hello World"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
