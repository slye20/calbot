import datetime
from zoneinfo import ZoneInfo
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import PRIMARY_CALENDAR_ID
from utils.auth import authenticate as auth

def get_events(max_results: int = 10, 
               search_query: Optional[str] = None, 
               days_from_now: Optional[int] = None):
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)

        pacific_tz = ZoneInfo("America/Los_Angeles")
        
        now = datetime.datetime.now(pacific_tz)
        
        # Calculate time range
        if days_from_now is not None:
            end_date = now + datetime.timedelta(days=days_from_now)
            time_max = end_date.isoformat()
        else:
            time_max = None
            
        now_pacific = now.isoformat()
        
        print(f"Getting events (Pacific time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')})")
        if search_query:
            print(f"Search query: '{search_query}'")
        
        # Build request parameters
        params = {
            "calendarId": PRIMARY_CALENDAR_ID,
            "timeMin": now_pacific,
            "timeZone": "America/Los_Angeles",
            "maxResults": max_results,
            "singleEvents": True,
            "orderBy": "startTime",
        }
        
        # Add optional parameters if provided
        if search_query:
            params["q"] = search_query
        if time_max:
            params["timeMax"] = time_max
            
        events_result = service.events().list(**params).execute()
        events = events_result.get("items", [])

        if not events:
            print("No events found matching criteria.")
            return "No events found matching your criteria."

        # Build a detailed string representation of the events
        events_info = []
        
        for i, event in enumerate(events, 1):
            # Get event details
            summary = event.get("summary", "Untitled event")
            location = event.get("location", "No location specified")
            description = event.get("description", "No description")
            
            # Format start time
            start = event["start"].get("dateTime", event["start"].get("date"))
            is_all_day = "T" not in start
            
            if is_all_day:
                start_display = start  # All-day event, keep as is
            else:
                event_time = datetime.datetime.fromisoformat(start)
                start_display = event_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            
            # Format end time
            end = event["end"].get("dateTime", event["end"].get("date"))
            if is_all_day:
                end_display = end  # All-day event, keep as is
            else:
                end_time = datetime.datetime.fromisoformat(end)
                end_display = end_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            
            # Get attendees if any
            attendees = event.get("attendees", [])
            attendee_list = []
            for attendee in attendees:
                email = attendee.get("email", "")
                name = attendee.get("displayName", email)
                attendee_list.append(name)
            
            attendees_str = ", ".join(attendee_list) if attendee_list else "No attendees"
            
            # Format the event information
            event_info = f"Event #{i}:\n"
            event_info += f"  Title: {summary}\n"
            event_info += f"  Start: {start_display}\n"
            event_info += f"  End: {end_display}\n"
            event_info += f"  Location: {location}\n"
            event_info += f"  Attendees: {attendees_str}\n"
            
            # Include event ID for potential operations
            event_info += f"  ID: {event['id']}\n"
            
            events_info.append(event_info)
        
        # Create a header
        header = f"Found {len(events)} event(s)"
        if search_query:
            header += f" matching '{search_query}'"
        if days_from_now:
            header += f" within the next {days_from_now} day(s)"
        header += ":\n\n"
        
        # Join all event information into a single string
        result = header + "\n".join(events_info)
        return result

    except HttpError as error:
        error_msg = f"An error occurred while fetching events: {error}"
        print(error_msg)
        return error_msg