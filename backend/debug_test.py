from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def check(url):
    print(f"Checking {url}...")
    try:
        r = client.get(url)
        print(f"Status: {r.status_code}")
        print(f"Headers: {r.headers}")
        print(f"Content (first 50): {r.text[:50]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

check("/")
check("/css/style.css")
check("/js/app.js")
check("/sw.js")
