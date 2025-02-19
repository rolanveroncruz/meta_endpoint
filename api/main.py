from fastapi import FastAPI, Request, Response
import json
import os
import logging
from pathlib import Path
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
    level=logging.INFO,  # Minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

logger = logging.getLogger(__name__)  # Get a logger instance

@app.get("/api/")
async def root():
    logger.info(f"/api called.")
    return {"whoami":"rolanvc.dev"}


@app.get("/api/meta_webhook")
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

@app.post("/webhook")
async def webhook(hub:dict):
    pass


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
