# import os
# from typing import Type

# from dotenv import load_dotenv
# from langchain.pydantic_v1 import BaseModel, Field
# from langchain_core.tools import BaseTool
# from slack_sdk.errors import SlackApiError
# from config import client  # Ensure your `client` is properly imported from config
# load_dotenv()

# # Pydantic models for tool arguments
# class DirectDMArgs(BaseModel):
#     message: str = Field(description="Should be a string containing the message to be sent to the Slack user")
#     user_id: str = Field(description="Should be a Slack user ID")


# # class GetAllUsers(BaseTool):
# #     name: str = "gets_all_users"
# #     description: str = "Useful for getting the SLACK IDs of users"

# #     def _run(self):
# #         """
# #         Gets the SLACK Ids of the users for sending the message.
# #         """
# #         all_users = {}
# #         try:
# #             # Call the users.list method
# #             response = client.users_list()
# #             members = response['members']

# #             # Iterate through the members and get their IDs and names
# #             for member in members:
# #                 user_id = member['id']
# #                 user_name = member['profile']['real_name']
# #                 all_users[user_name] = f"SLACK ID: {user_id}"
# #             return all_users
# #         except SlackApiError as e:
# #             print(f"Error fetching users: {e.response['error']}")
# #             return {}

# def GetAllUsers():
#     all_users = {}
#     try:
#         # Call the users.list method
#         response = client.users_list()
#         members = response['members']

#         # Iterate through the members and get their IDs and names
#         for member in members:
#             user_id = member['id']
#             user_name = member['profile']['real_name']
#             all_users[user_name] = user_id

#         return all_users
#     except SlackApiError as e:
#         print(f"Error fetching users: {e.response['error']}")
#         return {}

# class GetSingleUserSlackIDArgs(BaseModel):
#     name: str = Field(description="Should be the name of the user whom slack ID is need in string not dictionary")
    
# class GetSingleUserSlackID(BaseTool):
#     name: str = "gets_slack_id_single_user"
#     description: str = "Useful for getting the SLACK IDs of a single user based upon name"
#     args_schema: Type[BaseModel] = GetSingleUserSlackIDArgs
#     def _run(self, name:str):
#         all_users = GetAllUsers()
#         return str(all_users[name])

# class DirectDMTool(BaseTool):
#     name: str = "send_direct_dm"
#     description: str = "Useful for sending direct messages to Slack users within the channel"
#     args_schema: Type[BaseModel] = DirectDMArgs

#     def _run(self, message: str, user_id: str):
#         """
#         Sends a direct message to a Slack user in the channel.
#         """
#         try:
#             print(f"Message is: {message}")
#             print(f'Id is {user_id}')
#             client.chat_postMessage(channel=user_id, text=message)
#         except SlackApiError as e:
#             print(f"Error sending message: {e.response['error']}")

# # class DirectDMTool(BaseTool):
# #     name: str = "send_direct_dm"
# #     description: str = "Useful for sending direct messages to Slack users within the channel"
# #     args_schema: Type[BaseModel] = DirectDMArgs

# #     def _run(self, message: str, user_id: str):
# #         """
# #         Sends a direct message to a Slack user.
# #         """
# #         try:
# #             # Open a direct message channel with the user
# #             response = client.conversations_open(users=[user_id])
# #             channel_id = response['channel']['id']
# #             print(f"Channel id: {channel_id}")
# #             # Send the message to the channel
# #             print("Sending the message")
# #             print(f"Type: {type(channel_id)}")
# #             client.chat_postMessage(channel=channel_id, text=message)
            
# #             print(f"Message sent to user {user_id} in channel {channel_id}")
# #         except SlackApiError as e:
# #             print(f"Error sending message: {e.response['error']}")



# # Create tools using the Pydantic subclass approach

# tools = [
#     DirectDMTool(),
#     GetSingleUserSlackID()
# ]

# import json
# import os
# from typing import Type
# from dotenv import load_dotenv
# from langchain.pydantic_v1 import BaseModel, Field
# from langchain_core.tools import BaseTool
# from slack_sdk.errors import SlackApiError
# from datetime import datetime
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from services import construct_google_calendar_client
# from config import client
# load_dotenv()
# calendar_service = None
# # Pydantic models for tool arguments
# class DirectDMArgs(BaseModel):
#     message: str = Field(description="Should be a string containing the message to be sent to the Slack user")
#     user_id: str = Field(description="Should be a Slack user ID")

# class DateTimeTool(BaseTool):
#     name: str = "current_date_time"
#     description: str = "Provides the current date and time."

#     def _run(self):
#         """
#         Returns the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
#         """
#         return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# def GetAllUsers():
#     """
#     Gets all Slack users' names and Slack IDs.
#     """
#     all_users = {}
#     try:
#             # Call the users.list method
#             response = client.users_list()
#             members = response['members']

#             # Iterate through the members and get their IDs and names
#             for member in members:
#                 user_id = member['id']
#                 user_name = member['profile']['real_name']
#                 all_users[user_id] = user_name

#             return all_users
#     except SlackApiError as e:
#             print(f"Error fetching users: {e.response['error']}")
#             return {}

# class GetSingleUserSlackIDArgs(BaseModel):
#     name: str = Field(description="Should be the name of the user whose Slack ID is needed in string")

# class GetSingleUserSlackID(BaseTool):
#     name: str = "gets_slack_id_single_user"
#     description: str = "Useful for getting the SLACK IDs of a single user based on name"
#     args_schema: Type[BaseModel] = GetSingleUserSlackIDArgs

#     def _run(self, name: str):
#         all_users = GetAllUsers()
#         return str(all_users.get(name, "User not found"))
    
# class GetSingleUserSlackNameArgs(BaseModel):
#     id: str = Field(description="Should be the name of the user whose Slack ID is needed in string")

# class GetSingleUserSlackName(BaseTool):
#     name: str = "gets_slack_name_single_user"
#     description: str = "Useful for getting the SLACK name of a single user based on id"
#     args_schema: Type[BaseModel] = GetSingleUserSlackNameArgs

#     def _run(self, id: str):
#         all_users = GetAllUsers()
#         return str(all_users.get(id, "User not found"))

# class DirectDMTool(BaseTool):
#     name: str = "send_direct_dm"
#     description: str = "Useful for sending direct messages to Slack users within the channel"
#     args_schema: Type[BaseModel] = DirectDMArgs

#     def _run(self, message: str, user_id: str):
#         """
#         Sends a direct message to a Slack user in the channel.
#         """
#         try:
#             print(f"Message is: {message}")
#             print(f'Id is {user_id}')
#             client.chat_postMessage(channel=user_id, text=message)
#         except SlackApiError as e:
#             print(f"Error sending message: {e.response['error']}")

# # Google Calendar Tools



# class GoogleCalendarList(BaseTool):
#     name: str = "list_calendar_list"
#     description: str = "List available calendars in the user's Google Calendar account"
    
#     def _run(self, max_capacity: int = 200):
#         global calendar_service
#         calendar_service = construct_google_calendar_client('credentials.json', say)

#         """
#         Lists calendar lists until the total number of items reaches max_capacity.

#         Parameters:
#         - max_capacity (int): The maximum number of calendars to retrieve.
#         """
#         all_calendars = []
#         all_calendars_cleaned = []
#         next_page_token = None
#         capacity_tracker = 0

#         while True:
#             global calendar_service
#             calendar_list = calendar_service.calendarList().list(
#                 maxResults=min(200, max_capacity - capacity_tracker),
#                 pageToken=next_page_token
#             ).execute()
#             calendars = calendar_list.get('items', [])
#             all_calendars.extend(calendars)
#             capacity_tracker += len(calendars)
#             if capacity_tracker >= max_capacity:
#                 break
#             next_page_token = calendar_list.get('nextPageToken')
#             if not next_page_token:
#                 break

#         for calendar in all_calendars:
#             all_calendars_cleaned.append(
#                 {
#                     'id': calendar['id'],
#                     'name': calendar['summary'],
#                     'description': calendar.get('description', '')
#                 })

#         return all_calendars_cleaned

# class GoogleCalendarEvents(BaseTool):
#     name: str = "list_calendar_events"
#     description: str = "List events from a specific Google Calendar"
    
#     def _run(self, calendar_id: str = "primary", max_capacity: int = 20):
#         """
#         Lists events from a specific calendar.

#         Parameters:
#         - calendar_id (str): The calendar ID by default 'primary'.
#         - max_capacity (int): The maximum number of events to retrieve.
#         """
#         all_events = []
#         next_page_token = None
#         capacity_tracker = 0

#         while True:
#             global calendar_service
#             events_list = calendar_service.events().list(
#                 calendarId=calendar_id,
#                 maxResults=min(250, max_capacity - capacity_tracker),
#                 pageToken=next_page_token
#             ).execute()
#             events = events_list.get('items', [])
#             all_events.extend(events)
#             capacity_tracker += len(events)
#             if capacity_tracker >= max_capacity:
#                 break
#             next_page_token = events_list.get('nextPageToken')
#             if not next_page_token:
#                 break

#         return all_events

# class GoogleCreateCalendar(BaseTool):
#     name: str = "create_calendar_list"
#     description: str = "Creates a new calendar in Google Calendar"
    
#     def _run(self, calendar_name: str):
#         """
#         Creates a new calendar with the specified name.

#         Parameters:
#         - calendar_name (str): The name of the new calendar.
#         """
#         calendar_list = {
#             'summary': calendar_name
#         }
#         global calendar_service
#         created_calendar_list = calendar_service.calendarList().insert(body=calendar_list).execute()
#         return created_calendar_list

# class GoogleAddCalendarEventArgs(BaseModel):
#     calendar_id: str = Field(default="primary", description="The calendar ID where the event will be added (default is 'primary').")
#     summary: str = Field(description="The title or summary of the event.")
#     description: str = Field(default="", description="A description of the event.")
#     start_time: str = Field(description="The start time of the event in ISO 8601 format (e.g., '2025-01-22T10:00:00Z').")
#     end_time: str = Field(description="The end time of the event in ISO 8601 format (e.g., '2025-01-22T11:00:00Z').")
#     location: str = Field(default="", description="The location of the event (optional).")

# class GoogleAddCalendarEvent(BaseTool):
#     name: str = "add_calendar_event"
#     description: str = "Creates an event in a specified Google Calendar."
#     args_schema: Type[BaseModel] = GoogleAddCalendarEventArgs

#     def _run(self, summary: str, start_time: str, end_time: str,description: str = "",calendar_id: str = 'primary',location: str = ""):
#         """
#         Adds an event to the specified calendar.

#         Parameters:
#         - calendar_id (str): The calendar ID (default is 'primary').
#         - summary (str): The title of the event.
#         - description (str): A description of the event (based on text history).
#         - start_time (str): The start time in ISO 8601 format.
#         - end_time (str): The end time in ISO 8601 format.
#         - location (str): The location of the event (optional).
#         """
#         try:
#             event = {
#                 'summary': summary,
#                 'description': description,
#                 'start': {
#                     'dateTime': start_time,
#                     'timeZone': 'UTC',
#                 },
#                 'end': {
#                     'dateTime': end_time,
#                     'timeZone': 'UTC',
#                 },
#                 'location': location
#             }
#             global calendar_service
#             created_event = calendar_service.events().insert(calendarId=calendar_id, body=event).execute()
#             return {
#                 "id": created_event.get("id"),
#                 "status": "Event created successfully.",
#                 "link": created_event.get("htmlLink")
#             }
#         except Exception as e:
#             return {"error": str(e)}

# # Adding all tools into the tools array
# tools = [
#     # Slack Tools
#     DirectDMTool(),
#     GetSingleUserSlackName(),
#     # GetSingleUserSlackID(),
#     DateTimeTool(),
#     # Google Calendar Tools
#     GoogleCalendarList(),
#     GoogleCalendarEvents(),
#     GoogleCreateCalendar(),
#     GoogleAddCalendarEvent()
# ]
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
from services import construct_google_calendar_client
from config import client

load_dotenv()
calendar_service = None

# Pydantic models for tool arguments
class DirectDMArgs(BaseModel):
    message: str = Field(description="Should be a string containing the message to be sent to the Slack user")
    user_id: str = Field(description="Should be a Slack user ID")

class DateTimeTool(BaseTool):
    name: str = "current_date_time"
    description: str = "Provides the current date and time."

    def _run(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def GetAllUsers():
    all_users = {}
    try:
        response = client.users_list()
        members = response['members']
        for member in members:
            user_id = member['id']
            user_name = member['profile']['real_name']
            all_users[user_id] = user_name
        return all_users
    except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return {}
all_users = GetAllUsers()
class GetSingleUserSlackIDArgs(BaseModel):
    name: str = Field(description="Should be the name of the user whose Slack ID is needed in string")

class GetSingleUserSlackID(BaseTool):
    name: str = "gets_slack_id_single_user"
    description: str = "Useful for getting the SLACK IDs of a single user based on name"
    args_schema: Type[BaseModel] = GetSingleUserSlackIDArgs

    def _run(self, name: str):
        
        return str(all_users.get(name, "User not found"))
    
class GetSingleUserSlackNameArgs(BaseModel):
    id: str = Field(description="Should be the name of the user whose Slack ID is needed in string")

class GetSingleUserSlackName(BaseTool):
    name: str = "gets_slack_name_single_user"
    description: str = "Useful for getting the SLACK name of a single user based on id"
    args_schema: Type[BaseModel] = GetSingleUserSlackNameArgs

    def _run(self, id: str):
       
        return str(all_users.get(id, "User not found"))

class DirectDMTool(BaseTool):
    name: str = "send_direct_dm"
    description: str = "Useful for sending direct messages to Slack users within the channel"
    args_schema: Type[BaseModel] = DirectDMArgs

    def _run(self, message: str, user_id: str):
        try:
            client.chat_postMessage(channel=user_id, text=message)
            return "Message sent successfully"
        except SlackApiError as e:
            return f"Error sending message: {e.response['error']}"

# Google Calendar Tools
class GoogleCalendarList(BaseTool):
    name: str = "list_calendar_list"
    description: str = "List available calendars in the user's Google Calendar account"
    
    def _run(self, max_capacity: int = 200):
        global calendar_service
        if not calendar_service:
            calendar_service = construct_google_calendar_client('credentials.json')

        all_calendars = []
        next_page_token = None
        capacity_tracker = 0

        while capacity_tracker < max_capacity:
            results = calendar_service.calendarList().list(
                maxResults=min(200, max_capacity - capacity_tracker),
                pageToken=next_page_token
            ).execute()
            calendars = results.get('items', [])
            all_calendars.extend(calendars)
            capacity_tracker += len(calendars)
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        return [{
            'id': cal['id'],
            'name': cal['summary'],
            'description': cal.get('description', '')
        } for cal in all_calendars]

class GoogleCalendarEvents(BaseTool):
    name: str = "list_calendar_events"
    description: str = "List events from a specific Google Calendar"
    
    def _run(self, calendar_id: str = "primary", max_capacity: int = 20):
        global calendar_service
        if not calendar_service:
            calendar_service = construct_google_calendar_client('credentials.json')

        all_events = []
        next_page_token = None
        capacity_tracker = 0

        while capacity_tracker < max_capacity:
            results = calendar_service.events().list(
                calendarId=calendar_id,
                maxResults=min(250, max_capacity - capacity_tracker),
                pageToken=next_page_token
            ).execute()
            events = results.get('items', [])
            all_events.extend(events)
            capacity_tracker += len(events)
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        return all_events

class GoogleCreateCalendar(BaseTool):
    name: str = "create_calendar_list"
    description: str = "Creates a new calendar in Google Calendar"
    
    def _run(self, calendar_name: str):
        global calendar_service
        if not calendar_service:
            calendar_service = construct_google_calendar_client('credentials.json')

        calendar_body = {'summary': calendar_name}
        created_calendar = calendar_service.calendars().insert(body=calendar_body).execute()
        return f"Created calendar: {created_calendar['id']}"

class GoogleAddCalendarEventArgs(BaseModel):
    calendar_id: str = Field(default="primary", description="Calendar ID (default 'primary')")
    summary: str = Field(description="Event title")
    description: str = Field(default="", description="Event description")
    start_time: str = Field(description="Start time in ISO 8601 format")
    end_time: str = Field(description="End time in ISO 8601 format")
    location: str = Field(default="", description="Event location")

class GoogleAddCalendarEvent(BaseTool):
    name: str = "add_calendar_event"
    description: str = "Creates an event in a Google Calendar"
    args_schema: Type[BaseModel] = GoogleAddCalendarEventArgs

    def _run(self, summary: str, start_time: str, end_time: str, 
             description: str = "", calendar_id: str = 'primary', location: str = ""):
        global calendar_service
        if not calendar_service:
            calendar_service = construct_google_calendar_client('credentials.json')

        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
            'location': location
        }
        
        try:
            created_event = calendar_service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            return {
                "status": "success",
                "event_id": created_event['id'],
                "link": created_event.get('htmlLink', '')
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

tools = [
    DirectDMTool(),
    GetSingleUserSlackName(),
    GetSingleUserSlackID(),
    DateTimeTool(),
    GoogleCalendarList(),
    GoogleCalendarEvents(),
    GoogleCreateCalendar(),
    GoogleAddCalendarEvent()
]