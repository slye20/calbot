"""
Main entry point for the CalBot application.
"""

import utils.openai_client as openai_client
import utils.event_processor as event_processor

def process_user_request(user_message):
    """
    Process a user request from start to finish.
    
    Args:
        user_message: User's query as a string
        
    Returns:
        Results of any executed tool calls
    """
    # Create OpenAI client
    client = openai_client.create_openai_client()
    
    # Get AI response with tool calls
    input_messages, response = openai_client.get_ai_response(client, user_message)
    
    updated_messages = event_processor.process_tool_calls(response, input_messages)
    
    # Get AI summary of the results
    ai_response = openai_client.get_ai_text_response(client, updated_messages)
    
    return ai_response

if __name__ == "__main__":
    # user_query = input("How can I help with your calendar today? ")
    # user_query = "Create a new event for stanford class monday at 530pm."
    user_query = "Create a new event tomorrow at 8am for me to wake up."
    results = process_user_request(user_query)
    print(results)