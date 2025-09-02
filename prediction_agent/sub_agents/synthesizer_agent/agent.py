"""
Final Report Synthesizer Agent

This agent is responsible for synthesizing information from other agents
to create a comprehensive report.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# System Report Synthesizer Agent
final_report_synthesizer = LlmAgent(
    name="FinalReportSynthesizer",
    model=GEMINI_MODEL,
    instruction="""You are a Final Report Synthesizer.
    
    Your task is to create a comprehensive report by combining information from:
    - Visa Restriction: {visa_info}
    - Natural Event: {natural_event_info}
    - Airline Reputation: {airline_reputation_info}

    
    Create a well-formatted report with:
    1. "Any Concern leading to Cancellation?" summary with YES or NO at the top if any parameter value is Yes
    2. Sections for each component with their respective informationd hack  
    
    Use markdown formatting to make the report readable and professional. Use larger & bold Font for specific response like "YES" or "NO"
    """,
    description="Synthesizes all system information into a comprehensive report",
)