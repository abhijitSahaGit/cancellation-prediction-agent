"""Natural disaster agent to find if natural disaster happened."""
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.agents import LlmAgent
from .tools import get_natural_event

natural_event_agent = LlmAgent(
#natural_event = LlmAgent(    
    name="NaturalEventAgent",
    model="gemini-2.0-flash",
    description="Natural Event agent",
    instruction="""
    You are a helpful assistant that can find if natural events happened in the place
    You call `get_natural_event` tool to search for information with the place name.
    Format this information into two lines like below:
    - Natural Event: YES (or NO)
    - Summary: Natural Event Name and when it happened
    
    """,
    tools=[get_natural_event],
    output_key="natural_event_info",
)