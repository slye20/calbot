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
    Get a response from the AI model with the calendar tools for a new conversation.
    
    Args:
        client: OpenAI client instance
        user_message: User's query as a string
        
    Returns:
        Tuple of (input_messages, response)
    """
    # Start with system message including current date/time
    input_messages = [
        {"role": "system", "content": f"Today's date is {datetime.datetime.now()}. You are CalBot, an AI calendar assistant. For deleting events, please first search for the events then ask the user to confirm which one to delete."}
    ]
    
    # Add the current user message
    input_messages.append({"role": "user", "content": user_message})
    
    response = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=CALENDAR_TOOLS,
        tool_choice="auto"
    )
    
    return input_messages, response

def get_ai_response_with_history(client, messages):
    """
    Get a response from the AI model with the calendar tools using conversation history.
    
    Args:
        client: OpenAI client instance
        messages: List of conversation messages
        
    Returns:
        The OpenAI API response
    """
    # Make sure we have a system message
    has_system = any(msg.get("role") == "system" for msg in messages)
    if not has_system:
        messages.insert(0, {
            "role": "system", 
            "content": f"Today's date is {datetime.datetime.now()}. You are CalBot, an AI calendar assistant. For deleting events, please first search for the events then ask the user to confirm which one to delete."
        })
    
    return client.responses.create(
        model="gpt-4o",
        input=messages,
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