import services.get_events as get_events
import services.create_events as create_events
import services.cancel_events as cancel_events
import services.reschedule_events as reschedule_events

def main():
    """
    Main entry point for the calendar app.
    Uncomment the function you want to use:
    """
    # List upcoming events
    # return get_events.get_events()
    
    # Create a new event (random if none specified)
    # return create_events.create_event()
    
    # Cancel an event by search query
    # return cancel_events.cancel_event(query="Review")
    
    # Reschedule an event
    # Example 1: Search and reschedule via interactive prompt
    # return reschedule_events.reschedule_event(query="Review")
    
    # Example 2: Reschedule with specific date/time
    # return reschedule_events.reschedule_event(
    #     query="Review",
    #     start_date="2025-04-8",
    #     start_time="14:30"
    # )
    
    return None


if __name__ == "__main__":
    main()