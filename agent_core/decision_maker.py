# agent_core/decision_maker.py
# This module contains the core logic for classifying emails and deciding on actions.

import re

# --- Configuration for Classification Rules ---
# These lists can be expanded or moved to a config file later.
IMPORTANT_SENDERS = [
    "supervisor@example.com",
    "ceo@example.com"
]

SPAM_KEYWORDS = [
    "congratulations", "winner", "claim your prize", "free money", 
    "limited time offer", "100% free", "click here"
]

MEETING_KEYWORDS = ["meeting", "schedule", "calendar invite", "zoom link"]


def classify_email(email_data):
    """
    Analyzes an email's data and classifies it based on predefined rules.

    Args:
        email_data (dict): A dictionary containing parsed email details 
                           (sender, subject, body, etc.).

    Returns:
        str: The classification category (e.g., "IMPORTANT", "SPAM", "MEETING_REQUEST", "NORMAL").
    """
    sender = email_data.get('sender', '').lower()
    subject = email_data.get('subject', '').lower()
    body = email_data.get('body', '').lower()

    # Rule 1: Check for important senders
    # We use regex to find the email address, as the 'from' header can be "Name <email@addr.com>"
    for important_sender in IMPORTANT_SENDERS:
        if important_sender in sender:
            print(f"Classification: IMPORTANT (sender is {important_sender})")
            return "IMPORTANT"

    # Rule 2: Check for meeting-related keywords
    for keyword in MEETING_KEYWORDS:
        if keyword in subject or keyword in body:
            print(f"Classification: MEETING_REQUEST (found keyword: '{keyword}')")
            return "MEETING_REQUEST"

    # Rule 3: Check for spam keywords
    for keyword in SPAM_KEYWORDS:
        if keyword in subject or keyword in body:
            print(f"Classification: SPAM (found keyword: '{keyword}')")
            return "SPAM"

    # If no specific rules match, classify as NORMAL
    print("Classification: NORMAL (no specific rules matched)")
    return "NORMAL"

# This block allows for direct testing of the classification logic.
if __name__ == '__main__':
    print("--- Running Decision Maker Classification Test ---")

    # Create some sample email data to test our rules
    test_emails = [
        {
            'sender': 'Your Boss <supervisor@example.com>',
            'subject': 'URGENT: Project Update Required',
            'body': 'Please provide the latest numbers for Project X.'
        },
        {
            'sender': 'marketing@example-lottery.com',
            'subject': 'Congratulations! You are a winner!',
            'body': 'Click here to claim your prize.'
        },
        {
            'sender': 'colleague@example.com',
            'subject': 'Let us schedule a meeting for next week',
            'body': 'Hi, are you free to discuss the quarterly report?'
        },
        {
            'sender': 'newsletter@example.com',
            'subject': 'Your Weekly News Update',
            'body': 'Here is what happened this week.'
        }
    ]

    # Test each sample email
    for i, email in enumerate(test_emails):
        print(f"\n--- Testing Email {i+1} ---")
        print(f"From: {email['sender']}\nSubject: {email['subject']}")
        classification = classify_email(email)
        print(f"Final Classification Result: {classification}")
        print("-" * 20)

