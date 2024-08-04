import requests
import os
import json
import google.generativeai as genai
from transformers import pipeline

import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
classifier = pipeline('sentiment-analysis')


def is_toxic(content):
    prompt = f"Is the following statement toxic: '{content}'"
    result = classifier(prompt)
    responses = model.generate_content(prompt)
    if result[0]['label'] == 'NEGATIVE':
        return True
    return False


def generate_ai_reply(content):
    # Generate the AI reply
    prompt = f"Generate a reply to the following comment: '{content}'"
    responses = model.generate_content(prompt)
    return responses

