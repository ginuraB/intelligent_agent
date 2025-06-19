# integrations/email_service.py
# This module contains all functions for interacting with the Gmail API.

import base64
from email.mime.text import MIMEText
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
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        encoded_body = part.get('body', {}).get('data', '')
                        body = base64.urlsafe_b64decode(encoded_body).decode('utf-8')
                        break
            else:
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
    Creates and sends an email on behalf of the user.
    """
    try:
        service = get_google_api_service('gmail', 'v1')
        if not service:
            print("Failed to get Gmail service for sending email.")
            return

        # Create the email message object using MIMEText
        message = MIMEText(body_text)
        message['to'] = to
        message['subject'] = subject
        
        # The API requires the message to be base64url encoded
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encoded_message}
        
        # Call the API to send the email
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Email sent successfully. Message ID: {send_message['id']}")

    except HttpError as error:
        print(f"An error occurred while sending email: {error}")
    except Exception as e:
        print(f"An unexpected error occurred while sending email: {e}")

def modify_message_labels(message_id, labels_to_add=[], labels_to_remove=[]):
    """A helper function to add or remove labels from a message."""
    try:
        service = get_google_api_service('gmail', 'v1')
        if not service:
            print("Failed to get Gmail service for modifying labels.")
            return

        body = {
            'addLabelIds': labels_to_add,
            'removeLabelIds': labels_to_remove
        }
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        # print(f"Successfully modified labels for message {message_id}.")
        return True
    except HttpError as error:
        print(f"An error occurred while modifying labels: {error}")
        return False

def mark_as_read(message_id):
    """Marks a specific message as read by removing the 'UNREAD' label."""
    print(f"ACTION: Marking message {message_id} as read.")
    modify_message_labels(message_id, labels_to_remove=['UNREAD'])

def move_to_spam(message_id):
    """Moves a specific message to Spam by adding the 'SPAM' label."""
    print(f"ACTION: Moving message {message_id} to Spam.")
    modify_message_labels(message_id, labels_to_add=['SPAM'])

