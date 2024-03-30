import requests

server_url = "http://127.0.0.2:8000/summarize/"

def get_summary(text):
    response = requests.post(f"{server_url}?prompt={text}")
    return response