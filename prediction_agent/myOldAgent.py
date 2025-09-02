#from google.adk.agents import LlmAgent
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.natural_event.agent import natural_event
from .tools.weather_tool import get_weather
from .tools.twitter_tool import search_tweets
from .tools.visa import get_visa_restriction
from .tools.ama4dev_tools import search_flight_offers_tool, create_flight_order_tool
from .prompt import INSTRUCTION
from google.adk.agents import ParallelAgent, SequentialAgent
from .sub_agents.visa_info_agent import visa_info_agent
from .sub_agents.natural_event_agent import natural_event_agent

root_agent = Agent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="Agent to find if there is any red flag in end traveller's travel itinerary which might lead to booking cancellation.",
    instruction="""
    You are a orchestrator agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    **sub_agents:**
    You are responsible for delegating tasks to the following agent:
    - natural_event: If asked about natural event, you should use the google_search tool to search for the natural event in or around the city.
    **Tools:**
    You have access to the following tools to assist you:

    *   `search_flight_offers: Search for flight offers based on user input. Parameters: origin_city, destination_city, departure_date(YYYY-MM-DD). Returns a list of flight offers with details like price, flight number, and duration.
    *   `create_flight_order: Creates a flight order based on user input and selected flight offer. Parameter the flight offer ID of the offer the user selected from `search_flight_offers`. Ask for confirmation before executing this action.
    *   `get_weather: Retrieves the current weather report for a specified city.
    *   `search_tweets: Search for tweets based on user input.
    *   get_visa_restriction: Search Visa restriction for the country mentioned in users query
    
    Guidelines for 1.  *search_flight_offers:*
    *   Guide users through the flight booking process, including searching for flights, selecting options, and completing the booking.

    2. *Flight Search:*
    *   Search for flights based on user input, including origin city, destination city and departure date.
    *   Present flight options in a clear and organized manner. Easy to read and comprehend.
    *   While presenting flight options, include details like Airline name, Departure and Arrival time, Duration and Price.

    4. *Weather Information:*
    *   Provide current weather reports for specified cities to help users plan their travel.

    Guidelines for *Visa Information:*
    *   Find the country name from user's query and pass it to get_visa_restriction.
    """,
    #instruction=INSTRUCTION,
    sub_agents=[visa_info_agent, natural_event_agent],
    #tools=[AgentTool(natural_event), search_flight_offers_tool, create_flight_order_tool, get_weather, search_tweets, get_visa_restriction]
)
