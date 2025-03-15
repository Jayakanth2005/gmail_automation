import os
import base64
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import sys

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import get_db_connection

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API and return a service object."""
    flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def decode_base64(data):
    """Decodes base64-encoded email body."""
    try:
        return base64.urlsafe_b64decode(data).decode("utf-8")
    except Exception as e:
        print(f"⚠️ Base64 decoding error: {e}")
        return "Decoding Error"

def extract_email_body(payload):
    """Extracts the email body from text/plain or text/html content."""
    body_text = None
    body_html = None

    def extract_from_parts(parts):
        """Recursively extract email body from multipart messages."""
        nonlocal body_text, body_html
        for part in parts:
            mime_type = part.get('mimeType', '')
            body_data = part.get('body', {}).get('data', '')

            if mime_type == 'text/plain' and body_data:
                body_text = decode_base64(body_data)
            elif mime_type == 'text/html' and body_data:
                body_html = decode_base64(body_data)

            # Check nested parts (e.g., multipart/alternative)
            if 'parts' in part:
                extract_from_parts(part['parts'])

    # Check if the email has multiple parts
    if 'parts' in payload:
        extract_from_parts(payload['parts'])
    else:
        # Direct extraction if no 'parts'
        body_data = payload.get('body', {}).get('data', '')
        if body_data:
            body_text = decode_base64(body_data)

    # Return plain text if available, otherwise parse HTML content
    if body_text:
        return body_text.strip()
    elif body_html:
        return BeautifulSoup(body_html, "html.parser").get_text().strip()
    else:
        return "No Content Available"


def fetch_and_store_emails():
    """Fetch emails from Gmail API and store them in PostgreSQL."""
    service = authenticate_gmail()
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    # Fetch messages
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        print("\n🔍 Debugging Email Structure:")
        print(json.dumps(msg_data, indent=4))
        
        headers = {header['name']: header['value'] for header in msg_data['payload']['headers']}
        
        from_email = headers.get("From", "Unknown")
        to_email = headers.get("To", "Unknown")
        subject = headers.get("Subject", "No Subject")
        
        # Extract message body correctly
        message_body = extract_email_body(msg_data['payload'])

        # Debugging print statements
        print(f"\n--- Email ---\nFrom: {from_email}\nTo: {to_email}\nSubject: {subject}\nBody: {message_body[:500]}...\n")

        subject = subject[:255] if len(subject) > 255 else subject

        cursor.execute("""
                INSERT INTO emails (message_id, from_email, to_email, subject, message_body)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING;
            """, (msg['id'], from_email, to_email, subject, message_body))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Emails fetched and stored successfully!")

if __name__ == "__main__":
    fetch_and_store_emails()
