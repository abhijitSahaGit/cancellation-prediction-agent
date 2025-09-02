import requests
import os
from dotenv import load_dotenv
import json
from google.adk.tools import google_search
from googlesearch import search

load_dotenv()

MOCK_NATURAL_EVENT = os.getenv("MOCK_NATURAL_EVENT", "FALSE").upper() == "TRUE"
NATURAL_EVENT_FILE = "prediction_agent/data/natural_event.json"

def get_natural_event(place: str) -> dict:

    if MOCK_NATURAL_EVENT:
        natural_event = _load_natural_event()
        print(natural_event)
        event = natural_event.get(place, "No Natural event found")
        return {
            "status": "success",
            "restriction": f"The natural event in place {place}: {event}"
        }

def _load_natural_event()-> dict:
    """Load NATURAL_EVENT info from a JSON file"""
    try:
        with open(NATURAL_EVENT_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {NATURAL_EVENT_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {NATURAL_EVENT_FILE}")
        return {}