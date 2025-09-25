import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from utils.who_api_client import get_who_api_token
import requests

def search_for_chapter(token, query):
    # This is the official search endpoint
    search_url = "https://id.who.int/icd/release/11/2024-01/mms/search"
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json', 'Accept-Language': 'en', 'API-Version': 'v2'}
    params = {'q': query}

    try:
        print(f"ℹ️ Searching for '{query}' using the API search endpoint...")
        r = requests.get(search_url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        if 'destinationEntities' in data and len(data['destinationEntities']) > 0:
            print("\n--- Found Search Results ---")
            for entity in data['destinationEntities']:
                title = entity.get('title', 'No title')
                uri = entity.get('id', 'No URI')
                print(f"Title: {title}\nURI:   {uri}\n")
        else:
            print(f"❌ No search results found for the query '{query}'.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Could not perform search. {e}")

if __name__ == '__main__':
    print("--- Running ICD-11 Chapter Search Tool ---")
    api_token = get_who_api_token()
    if api_token:
        search_query = "Traditional Medicine"
        search_for_chapter(api_token, search_query)
    print("\n--- Search Complete ---")