"""
Main entry point for the CalBot application.
"""

import utils.openai_client as openai_client
import utils.event_processor as event_processor

def process_user_request(user_message, conversation=None):
    """
    Process a user request from start to finish.
    
    Args:
        user_message: User's query as a string
        conversation: Optional previous conversation history
        
    Returns:
        Tuple of (ai_response, updated_conversation)
    """
    # Create OpenAI client
    client = openai_client.create_openai_client()
    
    # Initialize conversation if needed
    if conversation is None:
        # Get AI response with tool calls for the first message
        input_messages, response = openai_client.get_ai_response(client, user_message)
    else:
        # Continue the conversation
        input_messages = conversation.copy()
        input_messages.append({"role": "user", "content": user_message})
        response = openai_client.get_ai_response_with_history(client, input_messages)
    
    # Process any tool calls
    updated_messages = event_processor.process_tool_calls(response, input_messages)
    
    # Get AI summary of the results
    ai_response = openai_client.get_ai_text_response(client, updated_messages)
    
    # Add the AI response to the conversation
    updated_messages.append({"role": "assistant", "content": ai_response})
    
    return ai_response, updated_messages

def interactive_session():
    """Run an interactive conversation session with the calendar bot."""
    print("CalBot - Your AI Calendar Assistant")
    print("-----------------------------------")
    print("Example commands:")
    print("- What events do I have tomorrow?")
    print("- Create a new event for team meeting tomorrow at 2pm")
    print("- Cancel my dentist appointment")
    print("- Reschedule my dentist appointment to 3pm")
    print("Type 'exit' to quit")
    print("-----------------------------------")
    
    # Initialize conversation
    conversation = None
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # Process the request and update conversation
        ai_response, conversation = process_user_request(user_input, conversation)
        
        # Print the AI response
        print(f"\nCalBot: {ai_response}")

if __name__ == "__main__":
    interactive_session()