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
    # url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key='
    data = {
        'comment': {'text': content},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = response.json()

    if 'attributeScores' in response_dict:
        score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        if score > 0.5:
            ai_reply = "Sorry, but your comment seems to be inappropriate."
        else:
            ai_reply = "Thank you for your comment!"
        return ai_reply
    else:
        return "Sorry, I couldn't generate a reply."
