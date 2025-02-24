"""
This script is to test Google Gemini's OCR capabilities.

"""
from google import genai
import PIL.Image
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv('GOOGLE_API_KEY')
def main():
    image=PIL.Image.open('data/receipt_cropped.png')
    client=genai.Client(api_key=GEMINI_API_KEY)
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

    response=client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[instructions, image],
    )
    print(response.text )


if __name__== "__main__":
    main()
