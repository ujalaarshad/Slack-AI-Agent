import json
import os
from typing import Type
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
from slack_sdk.errors import SlackApiError
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import client
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    creds = None
    token_dir = 'token_files'
    token_file = f'token.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(token_dir):
        os.mkdir(os.path.join(".", token_dir))
        
    if os.path.exists(os.path.join(token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(token_dir, token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(".", token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(".", token_dir, token_file))
        return None

# def construct_google_calendar_client(client_secret):
#     """
#     Constructs a Google Calendar API client.

#     Parameters:
#     - client_secret (str): The path to the client secret JSON file.

#     Returns:
#     - service: The Google Calendar API service instance.
#     """
#     API_NAME = 'calendar'
#     API_VERSION = 'v3'
#     service = create_service(client_secret, API_NAME, API_VERSION, SCOPES)
#     return service

# creds = None
# calendar_service = None
# if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#         creds = flow.run_local_server(port=8000)
#     with open("token.json", "w") as token:
#         token.write(creds.to_json())

# try:
#     calendar_service = build("calendar", "v3", credentials=creds)
# except Exception as e:
#     print(f"Failed to initialize Google Calendar API service: {e}")
def construct_google_calendar_client(client_secret):
    """
    Constructs Google Calendar API client with authorization checks and token handling.
    """
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    token_dir = 'token_files'
    token_path = os.path.join(token_dir, 'token.json')
    creds = None

    # Create token directory if needed
    if not os.path.exists(token_dir):
        os.makedirs(token_dir, exist_ok=True)

    # Try to load existing credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Validate or refresh credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            
            flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
            creds = flow.run_local_server(port=8000, open_browser=True)
            
        # Save new credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        return build(API_NAME, API_VERSION, credentials=creds, static_discovery=False)
    except Exception as e:
        
        print(f"API Error: {e}")
        return None
