from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import httpx
import requests

# Import WHO API client utils
from utils.who_api_client import get_who_api_token, search_icd11_term

app = FastAPI()

# Mount the frontend directory so all static files (CSS, JS, images) are accessible
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# WHO GHO Indicators
INDICATORS_URL = "https://ghoapi.azureedge.net/api/Indicator"

def fetch_indicators():
    resp = httpx.get(INDICATORS_URL)
    return resp.json()["value"]   # list of indicators

def search_indicator(query, indicators):
    query = query.lower()
    results = [
        ind for ind in indicators
        if query in ind["IndicatorName"].lower()
           or query in ind.get("ShortName","").lower()
    ]
    return results

# Serve dashboard.html at /dashboard.html
@app.get("/dashboard.html", response_class=HTMLResponse)
async def get_dashboard():
    path = os.path.join("frontend", "dashboard.html")
    if os.path.exists(path):
        return FileResponse(path)
    return HTMLResponse("<h1>404 - Dashboard Not Found</h1>", status_code=404)

# Optional: serve dashboard.html at root URL too
@app.get("/", response_class=HTMLResponse)
async def root():
    path = os.path.join("frontend", "dashboard.html")
    if os.path.exists(path):
        return FileResponse(path)
    return HTMLResponse("<h1>Welcome to the API</h1>", status_code=200)

# WHO API Proxy: fetch WHO data based on a query (indicator code)
@app.get("/api/who-data")
async def get_who_data(query: str = Query(..., description="Indicator code for WHO data")):
    url = f"https://ghoapi.azureedge.net/api/{query}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    if resp.status_code == 200:
        return resp.json()
    return {"error": "Could not fetch WHO data", "status_code": resp.status_code}

# WHO Indicator Search: search by name
@app.get("/api/search-indicators")
async def search_indicators(query: str = Query(..., description="Search term for WHO indicator")):
    indicators = fetch_indicators()
    results = search_indicator(query, indicators)
    return results

# Combined Search: GHO indicators + ICD-11 / TM11 terms
@app.get("/api/search-all")
async def search_all(query: str = Query(..., description="Search WHO GHO indicators and ICD-11 terms")):
    # GHO indicators
    indicators = fetch_indicators()
    gho_results = search_indicator(query, indicators)

    # ICD-11 search
    token = get_who_api_token()
    icd_results = search_icd11_term(token, query) if token else []

    return {"gho": gho_results, "icd11": icd_results}

# ICD-11 / TM11 details by URI
@app.get("/api/icd-details")
async def get_icd_details(uri: str = Query(..., description="ICD-11 entity URI")):
    token = get_who_api_token()
    if not token:
        return {"error": "WHO API token not available."}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "API-Version": "v2"
    }
    try:
        r = requests.get(uri, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch ICD details: {str(e)}"}
