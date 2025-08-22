import requests
import os
from dotenv import load_dotenv
from ..data.airports import Airport
from fuzzywuzzy import fuzz
import json

load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")
MOCK_AMA4DEV = os.getenv("MOCK_AMA4DEV").upper() == "TRUE"


AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
FLIGHT_CREATE_URL = "https://test.api.amadeus.com/v1/booking/flight-orders"
FLIGHT_OFFERS_FILE = "prediction_agent/tools/flight_offers_search_results.json"

traveler_info = {
    "id": "1",
    "dateOfBirth": "1988-02-15",
    "name": {"firstName": "John", "lastName": "Doe"},
    "gender": "MALE",
    "contact": {
        "emailAddress": "john.doe@email.com",
        "phones": [{
            "deviceType": "MOBILE",
            "countryCallingCode": "1",
            "number": "1234567890"
        }]
    },
    "documents": [{
        "documentType": "PASSPORT",
        "number": "123456789",
        "expiryDate": "2030-01-01",
        "issuanceCountry": "US",
        "nationality": "US",
        "holder": True
    }]
}


def search_flight_offers_tool(origin_city:str, destination_city:str, departure_date:str):

    if MOCK_AMA4DEV:
        print("Mocking flight search results")
        return _summarize_flight_offers(_load_flight_offers())
    
    token = _get_access_token()
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'originLocationCode': _match_location_to_code(origin_city),
        'destinationLocationCode': _match_location_to_code(destination_city),
        'departureDate': departure_date,
        'adults': 1,
        'nonStop': 'false',
        'currencyCode': 'INR',
        'max': 5
    }
    print(f"Calling Ama4DEV API with params: {params}")
    response = requests.get(FLIGHT_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"API call failed: {response.status_code}")
        print(response.text)
        _save_flight_offers([])
        return
    
    print(f"Ama4DEV API call succeeded: {response.status_code}")
    flight_offers = response.json().get('data', [])
    _save_flight_offers(flight_offers)
    return _summarize_flight_offers(flight_offers)


def create_flight_order_tool(flight_offer_id:str):

    if MOCK_AMA4DEV:
        print("Mocking flight order creation")
        return {"status": "success", "message": "Flight order created successfully"}

    flight_offer = _get_offer_by_id(flight_offer_id)
    if not flight_offer:
        return {"status": "error", "message": f"Flight offer with ID {flight_offer_id} not found"}

    _create_flight_order(traveler_info, flight_offer)

def _get_access_token():
    if not API_KEY or not API_SECRET:
        raise Exception("Missing API credentials.")
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(AUTH_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Auth failed: {response.status_code} {response.text}")

def _save_flight_offers(offers):
    """Save flight offers to a JSON file"""
    with open(FLIGHT_OFFERS_FILE, 'w') as f:
        json.dump(offers, f, indent=2)
    print(f"✅ Saved {len(offers)} flight offers to {FLIGHT_OFFERS_FILE}")


def _load_flight_offers():
    """Load flight offers from a JSON file"""
    try:
        with open(FLIGHT_OFFERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {FLIGHT_OFFERS_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {FLIGHT_OFFERS_FILE}")
        return []


def _get_offer_by_id(flight_id):
    """Fetch a flight offer from the JSON file by its string 'id'"""
    flight_offers = _load_flight_offers()
    for offer in flight_offers:
        if offer.get("id") == str(flight_id):
            return offer
    print(f"❌ No flight offer found with ID: {flight_id}")
    return None


def _create_flight_order(traveler_info, flight_offer):
    token = _get_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "data": {
            "type": "flight-order",
            "flightOffers": [flight_offer],
            "travelers": [traveler_info]
        }
    }
    response = requests.post(FLIGHT_CREATE_URL, headers=headers, json=payload)
    if response.status_code == 201:
        print("✅ Flight order created successfully!")
        print(response.json())
    else:
        print("❌ Flight order failed:")
        print(response.status_code, response.text)


def _summarize_flight_offers(offers):
    """Convert raw offers into a digestible summary list"""
    summaries = []
    for offer in offers:
        try:
            flight_id = offer.get("id")
            price = offer["price"]["total"]
            currency = offer["price"]["currency"]
            total_duration = offer["itineraries"][0]["duration"]

            first_segment = offer["itineraries"][0]["segments"][0]
            last_segment = offer["itineraries"][0]["segments"][-1]

            departure_time = first_segment["departure"]["at"]
            arrival_time = last_segment["arrival"]["at"]

            airline_code = first_segment.get("carrierCode")

            summary = {
                "id": flight_id,
                "airline": airline_code,
                "cost": f"{price} {currency}",
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "duration": total_duration.replace("PT", "").lower()
            }
            summaries.append(summary)
        except Exception as e:
            print(f"⚠️ Error processing offer ID {offer.get('id')}: {e}")
    return summaries


def _match_location_to_code(location):

    location = location.lower()
    best_match = None
    best_score = 0
    for loc_code, synonyms_set in Airport.items():
        max_score = max([fuzz.ratio(location, name.lower()) for name in synonyms_set])
        if max_score >= 80 and max_score>best_score:
            best_match = loc_code
            best_score = max_score
            if max_score == 100:
                break
    return best_match
