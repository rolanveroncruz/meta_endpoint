from fastapi import FastAPI, Request, Response
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
    challenge = request.query_params.get("hub.challenge", None)
    if mode is None or token is None or challenge is None:
        return Response(status_code=200)
    if token == verify_token:
        return Response(content=challenge, status_code=200)
    else:
        return Response(status_code=403)

@app.post("/webhook")
async def webhook(hub:dict):
    pass


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
