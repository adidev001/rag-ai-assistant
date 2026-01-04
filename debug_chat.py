import requests

url = "http://127.0.0.1:8000/chat/"
data = {"query": "what is yolo"}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Connection Error: {e}")
