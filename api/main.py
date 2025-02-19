from fastapi import FastAPI, Request
import json

app = FastAPI()


@app.get("/api/")
async def root():

    return {"whoami":"rolanvc.dev"}


@app.get("/api/meta_webhook")
async def meta_webhook(request:Request):
    """ This is the main endpoint for VERIFICATION REQUEST.
    Actually, it may also be the same endpoint for EVENT NOTIFICATION"""
    verify_token = "a7b3D9zX2kLqR1mN5pT8"
    mode = request.query_params.get("hub.mode", None)
    token = request.query_params.get("hub.verify_token", None)
    challenge = int(request.query_params.get("hub.challenge", None))
    if token == verify_token:
        return challenge

@app.post("/webhook")
async def webhook(hub:dict):
    pass


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
