"""
This script is to test Google Gemini's OCR capabilities.

"""
import ollama
import PIL.Image
import os
from dotenv import load_dotenv
import base64
import json
import requests

load_dotenv()

instructions = """
    Extract the following field:value pairs from the receipt and format them as a JSON object:
    Terminal No.
    Date and Time
    Type of Transaction
    Biller/Service
    Mobile Number
    Mobile Source
    Amount
    Service Fee
    Net Amount
    Total Amount
    Total Amount Inserted
"""


def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def parse_response(response_text):
    """Parse the response text from the model."""
    try:
        json_objects = response_text.splitlines()
        combined_result = []

        for json_object in json_objects:
            try:
                parsed_json = json.loads(json_object)
                content = parsed_json.get("message", {}).get("content", "")
                if content and content.strip():
                    combined_result.append(content.strip())
            except json.JSONDecodeError:
                combined_result.append(json_object.strip())

        joined_str= " ".join(combined_result)
        return joined_str

    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        return response_text


def perform_ocr(image_path):
    """Perform OCR on the given image using Llama 3.2-Vision."""
    base64_image = encode_image_to_base64(image_path)
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2-vision",
            "messages": [
                {
                    "role": "user",
                    "content": instructions,
                    "images": [base64_image],
                },
            ],
        }
    )
    if response.status_code == 200:
        return parse_response(response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    image_path = "data/receipt_cropped.png"
    response = perform_ocr(image_path)

    print(response)


if __name__== "__main__":
    main()
