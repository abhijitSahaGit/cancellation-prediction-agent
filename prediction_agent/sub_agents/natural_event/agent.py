from google.adk.agents import Agent
from google.adk.tools import google_search

natural_event = Agent(
    name="natural_event",
    model="gemini-2.0-flash",
    description="Natural Event agent",
    instruction="""
    You are a helpful assistant that can find if natural events happened in or around a city or nearby travel places of that city and will give if it is safe to travel that city around the given time.

    When asked about natural event, you should use the google_search tool to search for the natural event in or around the city.

    If the user ask for natural event without any city name and travel timeline, please asks for those missing parameters before you do the google serach query.
    """,
    tools=[google_search],
)