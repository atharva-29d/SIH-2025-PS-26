# AYUSH EMR Prototype (NAMASTE + ICD-11 Terminology Integration)

This is a prototype EMR dashboard for AYUSH clinicians with terminology search using NAMASTE and ICD-11 mappings.

## Features
- Doctor login with credentials
- Dashboard with doctor info & patient list
- Terminology search powered by FastAPI backend
- CSV ingest of NAMASTE + ICD mappings

## Credentials
- Username: `anjali` | Password: `ayurveda123`
- Username: `vikram` | Password: `siddha123`

## Setup

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run FastAPI
uvicorn main:app --reload

# 4. Open the app in your browser
http://127.0.0.1:8000/
