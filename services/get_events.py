import datetime
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import PRIMARY_CALENDAR_ID
from utils.auth import authenticate as auth

def get_events():
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)

        pacific_tz = ZoneInfo("America/Los_Angeles")
        
        now = datetime.datetime.now(pacific_tz)
        now_pacific = now.isoformat()
        
        print(f"Getting the upcoming 10 events (Pacific time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')})")
        
        events_result = (
            service.events()
            .list(
                calendarId=PRIMARY_CALENDAR_ID,
                timeMin=now_pacific,
                timeZone="America/Los_Angeles",
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            # Display in Pacific time format
            if "T" in start:  # This is a dateTime, not just a date
                event_time = datetime.datetime.fromisoformat(start)
                start_display = event_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_display = start  # All-day event, keep as is
            
            print(start_display, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")