# integrations/calendar_service.py
# This module contains all functions for interacting with the Google Calendar API.

from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
# Import our reusable authentication service
from integrations.auth_service import get_google_api_service

def create_calendar_event(summary, description, start_time, end_time, attendees=None):
    """
    Creates an event on the user's primary Google Calendar.

    Args:
        summary (str): The title of the event.
        description (str): The description of the event.
        start_time (datetime): The start date and time of the event.
        end_time (datetime): The end date and time of the event.
        attendees (list, optional): A list of attendee email addresses. Defaults to None.

    Returns:
        str: The HTML link to the created event, or None if it fails.
    """
    try:
        service = get_google_api_service('calendar', 'v3')
        if not service:
            print("Failed to get Calendar service. Aborting.")
            return None

        # The 'event' object is a dictionary that matches the structure
        # required by the Google Calendar API.
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Los_Angeles', # TODO: Make this configurable
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Los_Angeles', # TODO: Make this configurable
            },
        }

        # Add attendees if they are provided
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        print("Creating calendar event...")
        # Call the Calendar API's 'insert' method to create the event.
        # 'calendarId='primary'' refers to the user's main calendar.
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        event_link = created_event.get('htmlLink')
        print(f"Event created successfully! Link: {event_link}")
        return event_link

    except HttpError as error:
        print(f"An error occurred with the Calendar API: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# This block allows you to run this file directly for testing.
if __name__ == '__main__':
    print("--- Running Calendar Event Creation Test ---")
    
    # Define the details for our test event.
    # We'll create an event that starts in one hour and lasts for one hour.
    now = datetime.now()
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    # Call the function to create the event.
    create_calendar_event(
        summary='Agent Test Event',
        description='This is a test event created by the Intelligent Agent.',
        start_time=start_time,
        end_time=end_time,
        attendees=['uniginura@gmail.com'] # Optional: Add your own email here to test invites
    )
