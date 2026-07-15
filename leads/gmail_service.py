import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = os.path.join(settings.BASE_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'credentials.json')

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as f:
            creds = pickle.load(f)

    # auto-refresh expired token
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)

    if not creds or not creds.valid:
        raise Exception("No valid credentials found. Run gmail_auth.py first.")

    return build('gmail', 'v1', credentials=creds)