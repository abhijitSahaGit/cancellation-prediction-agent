#from google.adk.agents import LlmAgent
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools.weather_tool import get_weather
from .tools.twitter_tool import search_tweets
from .tools.visa import get_visa_restriction
from .tools.ama4dev_tools import search_flight_offers_tool, create_flight_order_tool
from .prompt import INSTRUCTION
from google.adk.agents import ParallelAgent, SequentialAgent
from .sub_agents.visa_info_agent import visa_info_agent
from .sub_agents.natural_event_agent import natural_event_agent
from .sub_agents.airline_reputation_agent import airline_reputation_agent
from .sub_agents.synthesizer_agent import final_report_synthesizer

# --- 1. Create Parallel Agent to gather information concurrently ---
multiple_info_gatherer = ParallelAgent(
    name="multiple_info_gatherer",
    sub_agents=[visa_info_agent, natural_event_agent, airline_reputation_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="final_report_agent",
    sub_agents=[multiple_info_gatherer, final_report_synthesizer],
)
