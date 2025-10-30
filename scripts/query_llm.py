import requests
import json

url = "http://localhost:8000/invoke"
headers = {"Content-Type": "application/json"}
payload = {
    "query": "What is a saving throw?",
    "thread_id": "test-session-1"
}

response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
if response.status_code == 200:
    for chunk in response.iter_content(chunk_size=None):
        print(chunk.decode('utf-8'), end='')
else:
    print(f"Error: {response.status_code} - {response.text}")