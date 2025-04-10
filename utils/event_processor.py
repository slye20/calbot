"""
Process tool calls returned by the OpenAI API and execute the corresponding calendar operations.
"""

import json
import services.get_events as get_events
import services.create_events as create_events
import services.cancel_events as cancel_events
import services.reschedule_events as reschedule_events

def process_tool_calls(response, input_messages):
    """
    Process tool calls from the OpenAI API response.
    
    Args:
        response: The OpenAI API response
        input_messages: The list of messages in the conversation
        
    Returns:
        Updated input_messages with tool call results
    """
    
    for tool_call in response.output:
        input_messages.append(tool_call)
        
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)
        result = execute_tool_call(name, args)
        
        # For passing back to the model, add the result as a string
        input_messages.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })
        
    
    return input_messages

def execute_tool_call(name, args):
    """
    Execute a specific tool call based on the name and arguments.
    
    Args:
        name: Name of the tool to call
        args: Arguments for the tool
        
    Returns:
        Result of the tool execution
    """
    if name == "get_events":
        return get_events.get_events(
            search_query=args["query"],
            max_results=args["max_results"],
            days_from_now=args["days_from_now"]
        )
    elif name == "create_event":
        event = {
            'summary': args["summary"],
            'location': args["location"],
            'description': args["description"],
            'start': {
                'dateTime': args["start_datetime"],
                'timeZone': args["timezone"],
            },
            'end': {
                'dateTime': args["end_datetime"], 
                'timeZone': args["timezone"],
            },
        }
        return create_events.create_event(event)
    elif name == "cancel_event":
        return cancel_events.cancel_event(event_id=args["event_id"])
    elif name == "reschedule_event":
        return reschedule_events.reschedule_event(
            event_id=args.get("event_id"),
            query=args.get("query"),
            start_date=args.get("start_date"),
            start_time=args.get("start_time"),
            duration_minutes=args.get("duration_minutes")
        )