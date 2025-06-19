# agent_core/main_agent.py
# This is the central control script that runs the agent's main loop.

import time
from config import SUPERVISOR_EMAIL, SLEEP_TIME_SECONDS
from agent_core.decision_maker import classify_email
from agent_core.text_parser import parse_meeting_details
from integrations.email_service import (
    fetch_unread_emails, 
    send_email, 
    mark_as_read, 
    move_to_spam
)
from integrations.calendar_service import create_calendar_event

def run_main_loop():
    """
    Runs the main operational loop of the intelligent agent.
    """
    print("--- Intelligent Agent is now running. Press Ctrl+C to stop. ---")
    print(f"Checking for new emails every {SLEEP_TIME_SECONDS} seconds.")

    try:
        while True:
            print("\n----------------------------------------------------")
            print(f"[{time.ctime()}] --- Checking for unread emails... ---")

            # 1. Perception: Fetch unread emails
            unread_emails = fetch_unread_emails()

            if not unread_emails:
                print("No new emails to process.")
            else:
                print(f"Found {len(unread_emails)} new email(s). Processing...")
                
                # 2. Decision Making: Process each email
                for email in unread_emails:
                    print(f"\n--- Analyzing Email ---")
                    print(f"From: {email.get('sender')}")
                    print(f"Subject: {email.get('subject')}")

                    classification = classify_email(email)

                    # 3. Action: Perform actions based on classification
                    if classification == "IMPORTANT":
                        print("ACTION: This is an important email. Escalating to supervisor.")
                        escalation_subject = f"URGENT: Agent Escalation - {email.get('subject')}"
                        escalation_body = (
                            "This email was flagged as important by the Intelligent Agent.\n\n"
                            f"Original Sender: {email.get('sender')}\n"
                            f"Original Subject: {email.get('subject')}\n\n"
                            "--- Original Email Body ---\n"
                            f"{email.get('body')}"
                        )
                        send_email(to=SUPERVISOR_EMAIL, subject=escalation_subject, body_text=escalation_body)
                        mark_as_read(email['id'])

                    elif classification == "MEETING_REQUEST":
                        print("ACTION: This is a meeting request. Attempting to parse details.")
                        # Combine subject and body for better parsing context
                        full_text = f"{email.get('subject', '')}\n{email.get('body', '')}"
                        event_details = parse_meeting_details(full_text)
                        
                        if event_details:
                            print(f"Parsed event details: {event_details['summary']} at {event_details['start_time']}")
                            # Create the calendar event
                            create_calendar_event(
                                summary=event_details['summary'],
                                description=f"Created from an email request.\n\n--- Original Email Snippet ---\n{email.get('snippet')}",
                                start_time=event_details['start_time'],
                                end_time=event_details['end_time'],
                                attendees=[email.get('sender')] # Automatically invite the sender
                            )
                        else:
                            print("Could not automatically parse meeting details. Manual action may be required.")
                        
                        mark_as_read(email['id'])

                    elif classification == "SPAM":
                        move_to_spam(email['id'])
                        
                    else: # NORMAL
                        mark_as_read(email['id'])
            
            # Wait for the next cycle
            print("\n--- Cycle complete. Waiting for next check... ---")
            time.sleep(SLEEP_TIME_SECONDS)

    except KeyboardInterrupt:
        print("\n--- Agent stopped by user. Goodbye! ---")

if __name__ == '__main__':
    run_main_loop()
