
import os
from dotenv import load_dotenv
import json

load_dotenv()

MOCK_AIRLINE_REPUTATION = os.getenv("MOCK_AIRLINE_REPUTATION", "FALSE").upper() == "TRUE"
AIRLINE_REPUTATION_FILE = "prediction_agent/data/airline_reputation.json"

def get_airline_reputation(airlineInfo: str) -> dict:
    print(f"\n**********************************************airlineInfo={airlineInfo}  : **********************************\n")
    if MOCK_AIRLINE_REPUTATION:
        airline_reputation = _load_airline_reputation()
        print(airline_reputation)
        reputation_info = airline_reputation.get(airlineInfo, "No Airline Reputation found")
        return {
            "status": "success",
            "reputation": f"Cancellation/Delay information found for airline {reputation_info}"
        }

def _load_airline_reputation()-> dict:
    """Load airline_reputation info from a JSON file"""
    try:
        with open(AIRLINE_REPUTATION_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {AIRLINE_REPUTATION_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {AIRLINE_REPUTATION_FILE}")
        return {}