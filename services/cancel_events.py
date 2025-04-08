import datetime
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import PRIMARY_CALENDAR_ID
from utils.auth import authenticate as auth

def find_event_by_query(query, max_results=10):
    """Search for events matching a query string in the summary or description."""
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)
        pacific_tz = ZoneInfo("America/Los_Angeles")
        now = datetime.datetime.now(pacific_tz)
        
        # Get events
        events_result = service.events().list(
            calendarId=PRIMARY_CALENDAR_ID,
            timeMin=now.isoformat(),
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
            q=query,  # Search term
            timeZone="America/Los_Angeles"
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            print(f"No events found matching '{query}'")
            return None
            
        print(f"Found {len(events)} event(s) matching '{query}':")
        for i, event in enumerate(events):
            start = event["start"].get("dateTime", event["start"].get("date"))
            if "T" in start:  # This is a dateTime, not just a date
                event_time = datetime.datetime.fromisoformat(start)
                start_display = event_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_display = start
                
            print(f"{i+1}. {start_display} - {event['summary']}")
            
        return events
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def cancel_event(event_id=None, query=None):
    """Cancel (delete) an event by ID or search query."""
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)
        
        # If we have a query but no ID, find the event first
        if event_id is None and query is not None:
            events = find_event_by_query(query)
            if not events:
                return None
                
            if len(events) > 1:
                # Ask which event to cancel if multiple found
                try:
                    choice = int(input("Enter the number of the event to cancel (0 to cancel): "))
                    if choice == 0:
                        print("Cancellation aborted.")
                        return None
                    if 1 <= choice <= len(events):
                        event_id = events[choice-1]["id"]
                    else:
                        print("Invalid selection.")
                        return None
                except ValueError:
                    print("Invalid input. Cancellation aborted.")
                    return None
            else:
                event_id = events[0]["id"]
                confirmation = input("Cancel this event? (y/n): ")
                if confirmation.lower() != 'y':
                    print("Cancellation aborted.")
                    return None
        
        if event_id:
            # Delete the event
            service.events().delete(
                calendarId=PRIMARY_CALENDAR_ID,
                eventId=event_id
            ).execute()
            
            print(f"Event with ID '{event_id}' has been cancelled.")
            return True
        else:
            print("No event ID provided for cancellation.")
            return None
            
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None 