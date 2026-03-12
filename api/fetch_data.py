import requests

BASE_URL = "https://www.cheapshark.com/api/1.0"

def fetch_all_deals(page_size):
    try:
        results = []
        response = requests.get(f"{BASE_URL}/deals?", params={"pageSize": page_size,})
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"error fetching data: {response.status_code}")
        return results
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def fetch_deal_by_id(deal_id):
    try:
        results = []
        response = requests.get(f"{BASE_URL}/deals",params={"id":deal_id})
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"error fetching data: {response.status_code}")
        return results
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def fetch_games_by_title(title):
    try:
        results = []
        response = requests.get(f"{BASE_URL}/games",params={"title": title})
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"Error fetching games for '{title}': {response.status_code}")
        return results
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def fetch_game_by_id(game_id):
    try:
        result = None
        response = requests.get(f"{BASE_URL}/games",params={"id": game_id})
        if response.status_code == 200:
            result = response.json()
        else:
            print(f"Error fetching game {game_id}: {response.status_code}")
        return result
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")
 
def fetch_all_stores():
    try:
        results = []
        response = requests.get(f"{BASE_URL}/stores")
        if response.status_code == 200:
            results = response.json()
        else:
            print(f"Error fetching stores: {response.status_code}")
        return results
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def set_price_alert(email, game_id, price):
    try:
        response = requests.get(f"{BASE_URL}/alerts",params={"action": "set","email": email,"gameID": game_id,"price": price,})
        if response.status_code == 200:
            print(f"Alert gesetzt für gameID {game_id} bei ${price} → {email}")
            return True
        else:
            print(f"Error setting alert: {response.status_code}")
            return False
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def delete_price_alert(email, game_id):
    try:
        response = requests.get(f"{BASE_URL}/alerts",params={"action": "delete","email": email,"gameID": game_id,})
        if response.status_code == 200:
            print(f"Alert gelöscht für gameID {game_id} → {email}")
            return True
        else:
            print(f"Error deleting alert: {response.status_code}")
            return False
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")