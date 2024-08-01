import requests
import os
import json

API_KEY = os.getenv('API_TOKEN_GEMINI')


def is_toxic(content):
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}'
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
            return True
        else:
            return False
    else:
        print('attributeScores not in response_dict')
        return False


def generate_ai_reply(content):
    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}'
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
