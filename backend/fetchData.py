import requests
from Cat import Cat

def fetch_data(cat):
    try:
        results = []
        response = requests.get(f"https://api.thecatapi.com/v1/images/search?limit={cat.limit}&page={cat.page}&order={cat.order}&has_breeds={cat.has_breeds}&breed_ids={cat.breed_ids}&category_ids={cat.category_ids}&sub_id={cat.sub_id}")
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"error fetching data: {response.status_code}")
        print(results)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

cat = Cat()

fetch_data(cat)