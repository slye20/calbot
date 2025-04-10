"""
Define the tool schemas for calendar operations to be used with OpenAI API.
"""

CALENDAR_TOOLS = [
    {
        "type": "function",
        "name": "get_events",
        "description": "Get events from the user's calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string", 
                    "description": "A search term to filter calendar events by text matching in title, description, location, etc. For example, 'workshop', 'meeting', 'doctor' or 'party'."
                },
                "max_results": {
                    "type": "number",
                    "description": "Maximum number of events to return. Default is 10."
                },
                "days_from_now": {
                    "type": "number",
                    "description": "Limit search to events within this many days from now. If not provided, no upper time limit is applied."
                }
            },
            "required": ["query", "max_results", "days_from_now"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "create_event",
        "description": "Create a new event on the user's calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Title or summary of the event"
                },
                "location": {
                    "type": "string",
                    "description": "Location where the event will take place. Default is San Francisco."
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the event. Default is 'No description provided.'"
                },
                "start_datetime": {
                    "type": "string",
                    "description": "Start date and time in ISO format (e.g., 'YYYY-MM-DDT14:00:00'). For relative times like 'tomorrow', the current date must be used as a reference."
                },
                "end_datetime": {
                    "type": "string",
                    "description": "End date and time in ISO format (e.g., 'YYYY-MM-DDT15:00:00'). For relative times like 'tomorrow', the current date must be used as a reference."
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone for the event. Default is 'America/Los_Angeles'."
                }
            },
            "required": ["summary", "location", "description", "start_datetime", "end_datetime", "timezone"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "cancel_event",
        "description": "Cancel an event on the user's calendar.",
        "parameters": {
            "type": "object",
            "properties": {
            "event_id": {
                "type": "string",
                "description": "The unique ID of the event to cancel. This is required."
            }
        },
        "required": ["event_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "reschedule_event",
        "description": "Reschedule an existing event on the user's calendar to a new time.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The unique ID of the event to reschedule. Optional if query is provided instead."
                },
                "query": {
                    "type": "string",
                    "description": "Search term to find the event to reschedule if event_id is not provided."
                },
                "start_date": {
                    "type": "string",
                    "description": "New date for the event in format YYYY-MM-DD or MM/DD/YYYY."
                },
                "start_time": {
                    "type": "string",
                    "description": "New time for the event in format HH:MM or HH:MM:SS, can include AM/PM."
                },
                "duration_minutes": {
                    "type": "number",
                    "description": "Duration of the event in minutes. If not provided, the original duration will be preserved."
                }
            },
            "required": ["event_id", "query", "start_date", "start_time", "duration_minutes"],
            "additionalProperties": False
        },
        "strict": True
    }
]