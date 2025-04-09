"""
Handle interactions with the OpenAI API.
"""

import datetime
from openai import OpenAI
from constants import OPENAI_API_KEY
from utils.calendar_tools import CALENDAR_TOOLS

def create_openai_client():
    """Create and return an OpenAI client instance."""
    return OpenAI(api_key=OPENAI_API_KEY)

def get_ai_response(client, user_message):
    """
    Get a response from the AI model with the calendar tools.
    
    Args:
        client: OpenAI client instance
        user_message: User's query as a string
        
    Returns:
        The OpenAI API response
    """
    # Start with system message including current date/time
    input_messages = [
        {"role": "system", "content": f"Today's date is {datetime.datetime.now()}"}
    ]
    
    # Add the current user message
    input_messages.append({"role": "user", "content": user_message})
    
    return input_messages, client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=CALENDAR_TOOLS,
        tool_choice="auto"
    )

def get_ai_text_response(client, updated_messages):
    """
    Get a text response from the AI model based on the conversation history.
    
    Args:
        client: OpenAI client instance
        updated_messages: List of messages including tool call results
        
    Returns:
        The AI's text response
    """
    response = client.responses.create(
        model="gpt-4o",
        input=updated_messages,
    )
    
    return response.output_text