import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

MOCK_VISA_RESTRICTION = os.getenv("MOCK_VISA_RESTRICTION", "FALSE").upper() == "TRUE"
VISA_RESTRICTION_FILE = "prediction_agent/data/visa_restriction.json"

def get_visa_restriction(country: str) -> dict:

    if MOCK_VISA_RESTRICTION:
        print("=========Mocking Visa restriction data========")
        visa_restrictions = _load_visa_restriction()
        print(visa_restrictions)
        restriction = visa_restrictions.get(country, "No restriction info available")
        return {
            "status": "success",
            "restriction": f"The VISA RESTRICTION for {country}: {restriction}"
        }

def _load_visa_restriction()-> dict:
    """Load Visa info from a JSON file"""
    try:
        with open(VISA_RESTRICTION_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {VISA_RESTRICTION_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {VISA_RESTRICTION_FILE}")
        return {}