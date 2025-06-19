# agent_core/text_parser.py
# A simple module to parse text for specific details using regular expressions.

import re
from datetime import datetime, timedelta

def parse_meeting_details(text):
    """
    A simple parser to extract meeting details (summary, date, time) from text.
    This is a basic implementation and can be significantly improved with more
    advanced NLP techniques.

    Args:
        text (str): The text content of an email (subject and body combined).

    Returns:
        dict: A dictionary with 'summary', 'start_time', and 'end_time', or None if not found.
    """
    summary = "Meeting"  # Default summary
    start_time = None

    # Try to find a subject for the meeting, often quoted or after keywords
    summary_match = re.search(r"(?:meeting about|discuss|topic:)\s*\'?\"?([^\'\"]+)\'?\"?", text, re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()

    # Very simple regex for time, e.g., "2pm", "10:30 AM"
    time_match = re.search(r"(\d{1,2}(?::\d{2})?)\s*(am|pm)", text, re.IGNORECASE)
    
    # Very simple regex for relative dates
    date_match_tomorrow = re.search(r"tomorrow", text, re.IGNORECASE)
    date_match_today = re.search(r"today", text, re.IGNORECASE)
    
    now = datetime.now()
    meeting_date = None

    if date_match_tomorrow:
        meeting_date = now + timedelta(days=1)
    elif date_match_today:
        meeting_date = now
    
    if meeting_date and time_match:
        time_parts = time_match.group(1).split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        period = time_match.group(2).lower()

        if period == 'pm' and hour < 12:
            hour += 12
        if period == 'am' and hour == 12:  # Handle midnight case (12 AM is 00:00)
            hour = 0

        # NEW: Add validation to prevent the ValueError crash
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            print(f"Error: Parsed an invalid time (hour={hour}, minute={minute}). Aborting parse.")
            return None
            
        start_time = meeting_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
    if start_time:
        # Assume a default duration of 1 hour for the meeting
        end_time = start_time + timedelta(hours=1)
        return {'summary': summary, 'start_time': start_time, 'end_time': end_time}

    # Return None if not enough details could be parsed
    return None
