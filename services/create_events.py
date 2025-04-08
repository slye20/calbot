import datetime
import random
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import PRIMARY_CALENDAR_ID
from utils.auth import authenticate as auth

def generate_random_event():
    """Generate a random event for testing purposes in Pacific time."""
    pacific_tz = ZoneInfo("America/Los_Angeles")
    
    # Get current time in Pacific timezone
    now = datetime.datetime.now(pacific_tz)
    
    # Generate a random start time between 1-7 days from now
    days_ahead = random.randint(1, 7)
    hours = random.randint(9, 17)  # Business hours 9am-5pm
    minutes = random.choice([0, 15, 30, 45])  # Quarter-hour increments
    
    # Create start time
    start_time = now + datetime.timedelta(days=days_ahead)
    start_time = start_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    
    # End time is 30-90 minutes after start time
    duration_minutes = random.choice([30, 45, 60, 90])
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)
    
    # Format as ISO strings with timezone
    start_str = start_time.isoformat()
    end_str = end_time.isoformat()
    
    # Generate random event details
    event_types = ["Meeting", "Call", "Review", "Interview", "Planning", "Workshop", "Presentation"]
    people = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley"]
    topics = ["Project X", "Quarterly Review", "New Feature", "Budget", "Roadmap", "Team Building"]
    
    event_type = random.choice(event_types)
    person = random.choice(people)
    topic = random.choice(topics)
    
    # Create event JSON
    event = {
        'summary': f"{event_type} with {person} about {topic}",
        'location': random.choice(['Conference Room A', 'Zoom Call', 'Coffee Shop', 'Office']),
        'description': f"Random test event created on {now.strftime('%Y-%m-%d')}",
        'start': {
            'dateTime': start_str,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_str,
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    return event

def create_event(event=None):
    creds = auth()
    try:
        service = build("calendar", "v3", credentials=creds)

        pacific_tz = ZoneInfo("America/Los_Angeles")
        
        now = datetime.datetime.now(pacific_tz)
        
        print(f"Creating event (current Pacific time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')})")
        
        # If no event provided, generate a random one
        if event is None:
            event = generate_random_event()
            print(f"Generated random event: {event['summary']}")
            print(f"Start: {event['start']['dateTime']}")
            print(f"End: {event['end']['dateTime']}")

        created_event = service.events().insert(calendarId=PRIMARY_CALENDAR_ID, body=event).execute()
        print('Event created: %s' % (created_event.get('htmlLink')))
        return created_event

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None