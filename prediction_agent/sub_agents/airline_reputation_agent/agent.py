"""This agent if the airline is prone to cancellation or delay"""
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from .tools import get_airline_reputation

airline_reputation_agent = LlmAgent(
#natural_event = LlmAgent(    
    name="AirlineReputationAgent",
    model="gemini-2.0-flash",
    description="Airline Reputation Agent checking Airline delay and cancellation",
    instruction="""
    1. You are a helpful assistant that can find if if the airline is prone to cancellation or delay.
    2. You call `get_airline_reputation` tool to search for information with the below input format.
        Input Format to `get_airline_reputation` tool: "Airline Name SourceCity-DestinationCity"
            Example: "Thai Airways Bengaluru-Bangkok"
        
        Output Format of Response of is below:
            "Cancellations": "Extremely Rare, Rare, Common or Moderate or Frequent",
            "Average Delay": "~x minutes",
            "Punctuality Rate": "~y%"
            Example:
                "Thai Airways Bengaluru-Bangkok": {
                    "Cancellations": "Extremely Rare – No reported cancellations",
                    "Average Delay": "20 minutes",
                    "Punctuality Rate": "~85%"
                }
    3. Generate Response in below Format following the given instruction in point#4
    - Issue with Airline Reputation(cancellation or delay): YES (or NO)
    - Summary: Share the complete response got `get_airline_reputation` tool in points
    4. Instruction to decide Issue with Airline Reputation(cancellation or delay): Yes (or No)
        If "Cancellation" is Rare or Extremely Rare, that means No Issue
        If "Average Delay" is less than 30 minutes, that means No Issue
    """,
    tools=[get_airline_reputation],
    output_key="airline_reputation_info",
)
