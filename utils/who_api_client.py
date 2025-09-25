import os
import requests
from dotenv import load_dotenv


def get_who_api_token():
    load_dotenv()
    token_url = 'https://icdaccessmanagement.who.int/connect/token'
    client_id = os.getenv('WHO_CLIENT_ID')
    client_secret = os.getenv('WHO_CLIENT_SECRET')
    if not client_id or not client_secret or "your_client_id" in client_id:
        print("⚠️  WARNING: WHO credentials not set in .env file.")
        return None
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret,
               'scope': 'icdapi_access'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        r = requests.post(token_url, data=payload, headers=headers, timeout=10)
        r.raise_for_status()
        print("✅ Successfully obtained WHO API Token.")
        return r.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Could not get WHO API token. {e}")
        return None


def search_icd11_term(token, query):
    """
    Searches the ICD-11 API for a given term.
    """
    if not token or not query: return []
    search_url = "https://id.who.int/icd/release/11/2024-01/mms/search"
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json', 'Accept-Language': 'en',
               'API-Version': 'v2'}
    params = {'q': query}

    try:
        r = requests.get(search_url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        # Return the list of matching entities found by the API
        if 'destinationEntities' in data:
            print(f"ℹ️ API search for '{query}' returned {len(data['destinationEntities'])} results.")
            return data['destinationEntities']
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Could not perform WHO API search. {e}")
        return []