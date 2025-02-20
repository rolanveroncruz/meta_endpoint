from fastapi import FastAPI, Request, Response
import json
import os
import logging
from pathlib import Path
import hmac
import hashlib
from dotenv import load_dotenv
import requests

load_dotenv()
APP_SECRET = os.getenv("AI_CHAT_APP_SECRET")
APP_TOKEN = os.getenv("AI_CHAT_APP_TOKEN2")
app = FastAPI()
# Configure logging
the_current_directory = Path(__file__).parent
log_directory = os.path.join(the_current_directory, "logs")  # Directory to store logs
print(log_directory)
log_file_path = os.path.join(log_directory, "fastapi.log")

# Create the log directory if it doesn't exist
Path(log_directory).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_file_path,  # Log file path
    level=logging.DEBUG,  # Minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

logger = logging.getLogger(__name__)  # Get a logger instance

@app.get("/api/")
async def root():
    logger.info(f"/api called.")
    return {"whoami":"rolanvc.dev"}


@app.get("/api/webhook")
async def meta_webhook(request:Request):
    """ This is the main endpoint for VERIFICATION REQUEST.
    Actually, it may also be the same endpoint for EVENT NOTIFICATION"""
    verify_token = "a7b3D9zX2kLqR1mN5pT8"
    mode = request.query_params.get("hub.mode", None)
    logger.info(f"mode: {mode}")
    token = request.query_params.get("hub.verify_token", None)
    logger.info(f"token: {token}")
    challenge = request.query_params.get("hub.challenge", None)
    logger.info(f"challenge: {challenge}")
    if mode is None or mode != 'subscribe' or token is None or challenge is None:
        logger.info(f"returning: 403")
        return Response(status_code=403)
    if token == verify_token:
        logger.info(f"token and verify_token_match, returning: {challenge}")
        return Response(content=challenge, status_code=200)
    else:
        logger.info(f"mismatch in token:{token} & verify token:{verify_token}::: {challenge}")
        return Response(status_code=403)

@app.post("/api/webhook")
async def webhook(request:Request):
    logger.info(f" ")
    logger.info(f" ")
    logger.info(f" ")
    logger.info(f"/api/webhook called. ")
    # first validata payload
    # 1. generate SHA-256 signature from payload and app secret.
    # 2. compare with secret.
    request_body = await request.body()
    secret = os.getenv("AI_CHAT_APP_SECRET")
    request_json= await request.json()
    logger.info(f"request_json: {request_json}")
    x_hub_signature_sha256 = request.headers.get("x-hub-signature-sha256", None)
    secret_byte_array = bytes(secret, encoding="utf-8")

    signature = hmac.new(secret_byte_array, request_body, hashlib.sha256).hexdigest()
    logger.info(f"signature: {signature}")


    if x_hub_signature_sha256 is None:
        logger.info(f"can't find x_hub_signature_sha256 in headers")
    else:
        logger.info(f"x_hub_signature_sha256: {x_hub_signature_sha256}")

    object = request_json["object"]
    if object and object == 'page':
        logger.info(f"object: {object}")
        entries = request_json["entry"]
        for entry in entries:
            logger.debug(f"entry: {entry}")
            if 'messaging' in entry:
                messages=entry['messaging']
                for entry_message in messages:
                    logger.debug(f"entry_message: {entry_message}")
                    sender = entry_message.get("sender", None)
                    sender_id=""
                    if sender is not None:
                        sender_id = sender.get("id", None)
                        try:
                            get_url=f"https://graph.facebook.com/{sender_id}?fields=first_name,last_name&token={APP_TOKEN}"
                            request = requests.get(get_url)
                        except Exception as e:
                            logger.error(f"get_url: {get_url}")
                            logger.error(f"requests.get: {e}")
                        logger.info(f"get_url: {get_url}")
                        logger.info(f"request: {request}")
                    timestamp = entry_message.get("timestamp", 0)
                    message = entry_message["message"]
                    if message is not None:
                        message_text = message.get("text", None)
                        logger.info(f" received message (sender_id:{sender_id}, text: {message_text}, at timestamp: {timestamp}) ")

    return Response(status_code=200)




@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
