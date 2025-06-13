# integrations/email_service.py
# This module contains all functions for interacting with the Gmail API.

import base64
from googleapiclient.errors import HttpError
# Import the authentication service we created
from integrations.auth_service import get_google_api_service

def fetch_unread_emails():
    """
    Fetches all unread emails from the user's inbox, parses them,
    and returns a list of email data.
    """
    try:
        service = get_google_api_service('gmail', 'v1')
        if not service:
            print("Failed to get Gmail service. Aborting.")
            return []

        # List all unread messages
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])

        if not messages:
            print("No unread messages found.")
            return []

        print(f"Found {len(messages)} unread messages. Fetching details...")
        
        email_list = []
        for message_info in messages:
            msg = service.users().messages().get(userId='me', id=message_info['id']).execute()
            payload = msg.get('payload', {})
            headers = payload.get('headers', [])
            
            # Extract sender, recipient, and subject from headers
            email_data = {
                'id': msg.get('id'),
                'threadId': msg.get('threadId'),
                'snippet': msg.get('snippet'),
                'sender': '',
                'recipient': '',
                'subject': ''
            }
            for header in headers:
                name = header.get('name', '').lower()
                if name == 'from':
                    email_data['sender'] = header.get('value')
                elif name == 'to':
                    email_data['recipient'] = header.get('value')
                elif name == 'subject':
                    email_data['subject'] = header.get('value')

            # Get the email body
            body = ''
            if 'parts' in payload:
                # This handles multipart emails (e.g., with attachments or both text and html)
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        encoded_body = part.get('body', {}).get('data', '')
                        body = base64.urlsafe_b64decode(encoded_body).decode('utf-8')
                        break
            else:
                # This handles simple, single-part emails
                encoded_body = payload.get('body', {}).get('data', '')
                if encoded_body:
                    body = base64.urlsafe_b64decode(encoded_body).decode('utf-8')
            
            email_data['body'] = body
            email_list.append(email_data)
        
        print("Finished fetching email details.")
        return email_list

    except HttpError as error:
        print(f"An error occurred with the Gmail API: {error}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def send_email(to, subject, body_text):
    """
    Sends an email on behalf of the user.
    (This is a placeholder function to be fully implemented later)
    """
    print(f"\n--- (SIMULATION) ---")
    print(f"Attempting to send email to: {to}")
    print(f"Subject: {subject}")
    print("This function will be implemented in a future step.")
    print("--------------------")
    # TODO: Implement the full email sending logic using MIMEText and the API.
    pass


def list_gmail_labels():
    """
    Connects to the Gmail API and lists the user's labels.
    This is a test function to verify that authentication is working.
    """
    try:
        service = get_google_api_service('gmail', 'v1')
        if not service:
            print("Failed to get Gmail service. Aborting.")
            return

        print("\nAttempting to call the Gmail API to list labels...")
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        
        print('\nGmail Labels:')
        for label in labels:
            print(f"- {label['name']} (ID: {label['id']})")
        print("\nSuccessfully connected to Gmail and fetched labels!")

    except HttpError as error:
        print(f"An error occurred with the Gmail API: {error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    print("--- Running Email Fetching Test ---")
    unread_emails = fetch_unread_emails()
    if unread_emails:
        print(f"\n--- Successfully fetched {len(unread_emails)} email(s) ---")
        # Print details of the first email as a sample
        first_email = unread_emails[0]
        print(f"From: {first_email['sender']}")
        print(f"Subject: {first_email['subject']}")
        print(f"Snippet: {first_email['snippet']}")
        print("-" * 20)

