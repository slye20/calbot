import datetime
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import PRIMARY_CALENDAR_ID
from utils.auth import authenticate as auth
from services.cancel_events import find_event_by_query

def parse_datetime(date_str, time_str):
    """Parse date and time strings into a datetime object."""
    pacific_tz = ZoneInfo("America/Los_Angeles")
    
    # Parse date
    try:
        # Try common formats
        if "-" in date_str:
            # YYYY-MM-DD
            year, month, day = map(int, date_str.split("-"))
        elif "/" in date_str:
            # MM/DD/YYYY or DD/MM/YYYY (assuming MM/DD/YYYY for US)
            parts = date_str.split("/")
            if len(parts[2]) == 4:  # Assume MM/DD/YYYY
                month, day, year = map(int, parts)
            else:
                day, month, year = map(int, parts)
        else:
            raise ValueError("Unknown date format")
        
        # Parse time
        if ":" in time_str:
            # HH:MM or HH:MM:SS
            time_parts = time_str.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            second = int(time_parts[2]) if len(time_parts) > 2 else 0
            
            # Handle AM/PM
            if "pm" in time_str.lower() and hour < 12:
                hour += 12
            if "am" in time_str.lower() and hour == 12:
                hour = 0
        else:
            # Assume just hours
            hour = int(time_str)
            minute = 0
            second = 0
        
        # Create datetime
        return datetime.datetime(year, month, day, hour, minute, second, tzinfo=pacific_tz)
    
    except Exception as e:
        print(f"Error parsing date/time: {e}")
        return None

def reschedule_event(event_id=None, query=None, new_start_time=None, new_end_time=None, 
                     duration_minutes=None, start_date=None, start_time=None):
    """
    Reschedule an event by updating its start and end times.
    
    Args:
        event_id: The ID of the event to reschedule
        query: Search term to find the event if ID is not provided
        new_start_time: New start time as a datetime object
        new_end_time: New end time as a datetime object
        duration_minutes: If provided, end time will be calculated based on duration
        start_date: String date format (alternative to new_start_time)
        start_time: String time format (alternative to new_start_time)
    """
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)
        event = None
        
        # First, get the event
        if event_id is None and query is not None:
            events = find_event_by_query(query)
            if not events:
                return None
                
            if len(events) > 1:
                # Ask which event to reschedule if multiple found
                try:
                    choice = int(input("Enter the number of the event to reschedule (0 to cancel): "))
                    if choice == 0:
                        print("Rescheduling aborted.")
                        return None
                    if 1 <= choice <= len(events):
                        event = events[choice-1]
                        event_id = event["id"]
                    else:
                        print("Invalid selection.")
                        return None
                except ValueError:
                    print("Invalid input. Rescheduling aborted.")
                    return None
            else:
                event = events[0]
                event_id = event["id"]
                confirmation = input(f"Reschedule this event? (y/n): ")
                if confirmation.lower() != 'y':
                    print("Rescheduling aborted.")
                    return None
        elif event_id:
            # Get the event by ID
            event = service.events().get(
                calendarId=PRIMARY_CALENDAR_ID,
                eventId=event_id
            ).execute()
        
        if not event:
            print("No event found to reschedule.")
            return None
            
        # Parse start/end times if provided as strings
        if start_date and start_time:
            new_start_time = parse_datetime(start_date, start_time)
            if not new_start_time:
                return None
        
        # If we have new start time, update the event
        if new_start_time:
            pacific_tz = ZoneInfo("America/Los_Angeles")
            
            # Get original event duration if not specified
            if not new_end_time and not duration_minutes:
                orig_start = event["start"].get("dateTime")
                orig_end = event["end"].get("dateTime")
                
                if orig_start and orig_end:
                    start_dt = datetime.datetime.fromisoformat(orig_start.replace('Z', '+00:00'))
                    end_dt = datetime.datetime.fromisoformat(orig_end.replace('Z', '+00:00'))
                    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
                else:
                    # Default to 30 minutes if we can't determine
                    duration_minutes = 30
            
            # Calculate end time
            if not new_end_time and duration_minutes:
                new_end_time = new_start_time + datetime.timedelta(minutes=duration_minutes)
            
            # Update the event
            event["start"]["dateTime"] = new_start_time.isoformat()
            event["end"]["dateTime"] = new_end_time.isoformat()
            
            updated_event = service.events().update(
                calendarId=PRIMARY_CALENDAR_ID,
                eventId=event_id,
                body=event
            ).execute()
            
            print("Event rescheduled:")
            print(f"Title: {updated_event['summary']}")
            print(f"New start: {new_start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"New end: {new_end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"Link: {updated_event.get('htmlLink')}")
            
            return updated_event
        else:
            print("No new start time provided for rescheduling.")
            return None
            
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None 