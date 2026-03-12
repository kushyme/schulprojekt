import requests

def fetch_data():
    try:
        results = []
        response = requests.get(f"")
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"error fetching data: {response.status_code}")
        print(results)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")