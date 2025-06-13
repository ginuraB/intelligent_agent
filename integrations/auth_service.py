# integrations/auth_service.py
# This module handles the OAuth 2.0 authentication flow for all Google APIs.

import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the SCOPES (permissions) your agent will need.
# If you modify these scopes, you must delete the existing token.json file.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",      # Read emails
    "https://www.googleapis.com/auth/gmail.send",          # Send emails
    "https://www.googleapis.com/auth/gmail.modify",        # Modify emails (e.g., mark as read)
    "https://www.googleapis.com/auth/calendar",            # Full calendar access
    "https://www.googleapis.com/auth/drive"                # Full Google Drive access
]

# Define the path to your credentials and token files.
# Make sure credentials.json is in the 'credentials' folder at the project root.
CREDENTIALS_FILE = os.path.join(os.getcwd(), 'credentials', 'credentials.json')
TOKEN_FILE = os.path.join(os.getcwd(), 'credentials', 'token.json')


def get_google_api_service(api_name, api_version):
    """
    Authenticates with the Google API and returns a service object.
    Handles the OAuth 2.0 flow, including token storage and refresh.

    Args:
        api_name (str): The name of the API to connect to (e.g., 'gmail', 'calendar', 'drive').
        api_version (str): The version of the API (e.g., 'v1', 'v3').

    Returns:
        A Google API service object, or None if authentication fails.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Error loading credentials from token file: {e}")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials have expired. Refreshing token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}. Please re-authenticate.")
                # If refresh fails, force re-authentication by setting creds to None
                creds = None
        else:
            print("No valid credentials found. Starting authentication flow...")
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERROR: credentials.json not found at {CREDENTIALS_FILE}")
                print("Please download it from Google Cloud Console and place it correctly.")
                return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Failed to run authentication flow: {e}")
                return None

        # Save the credentials for the next run
        print("Authentication successful. Saving credentials to token.json...")
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print(f"Credentials saved to {TOKEN_FILE}")
        except Exception as e:
            print(f"Error saving credentials: {e}")

    try:
        service = build(api_name, api_version, credentials=creds)
        print(f"Successfully connected to {api_name} API version {api_version}.")
        return service
    except HttpError as error:
        print(f"An error occurred while building the service: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

