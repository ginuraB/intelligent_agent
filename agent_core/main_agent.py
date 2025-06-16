# agent_core/main_agent.py
# This is the central control script that runs the agent's main loop.

import time
from config import SUPERVISOR_EMAIL, SLEEP_TIME_SECONDS
from agent_core.decision_maker import classify_email
from integrations.email_service import fetch_unread_emails
# We will import these later when we implement actions
# from integrations.calendar_service import create_calendar_event
# from integrations.file_service import upload_file_to_drive

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

                    # 3. Action (Placeholder): Decide what action to take based on classification
                    # In the future, this section will call other services.
                    if classification == "IMPORTANT":
                        print("ACTION: This is an important email. Escalating to supervisor.")
                        # TODO: Call email_service.send_email to notify SUPERVISOR_EMAIL
                    elif classification == "MEETING_REQUEST":
                        print("ACTION: This is a meeting request.")
                        # TODO: Call a function to parse date/time and then use calendar_service
                    elif classification == "SPAM":
                        print("ACTION: This is spam.")
                        # TODO: Call email_service.move_to_spam(email['id'])
                    else: # NORMAL
                        print("ACTION: No special action required. Marking as read.")
                        # TODO: Call email_service.mark_as_read(email['id'])
            
            # Wait for the next cycle
            print("\n--- Cycle complete. Waiting for next check... ---")
            time.sleep(SLEEP_TIME_SECONDS)

    except KeyboardInterrupt:
        print("\n--- Agent stopped by user. Goodbye! ---")

if __name__ == '__main__':
    run_main_loop()
