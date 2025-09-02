"""Visa information agent to find visa retriction."""

from google.adk.agents import LlmAgent

from .tools import get_visa_restriction

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# CPU Information Agent
visa_info_agent = LlmAgent(
    name="VisaInfoAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Visa Information Agent.
    
    When asked for Visa information, you should:
    1. Use the 'get_visa_restriction' tool to gather Visa information
    2. Analyze the returned Visa information to find if any VISA restriction is there
    3. Format this information into two lines like below:
    - Visa Restriction: YES, Restriction found (or NO, Restriction Found)
    - Summary: Summarization of Visa information or restriction in one line
    
    IMPORTANT: You MUST call the get_visa_restriction. If any specific restriction or rule found for the contry then only raise concern. No concern should be raised for entry free or normal Visa rules countries
    """,
    description="Gathers and analyzes Visa information",
    tools=[get_visa_restriction],
    output_key="visa_info",
)