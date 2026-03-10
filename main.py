import requests

def fetch_data(limit=1):
    try:
        results = []
        response = requests.get(f"https://api.thecatapi.com/v1/images/search?limit={limit}?mime_types=gif")
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"error fetching data: {response.status_code}")
        print(results)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

fetch_data()