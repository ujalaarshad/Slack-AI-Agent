import os
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from agents import agent_exec
from config import client, SLACK_BOT_TOKEN
from prompt import event_details

# Load environment variables
load_dotenv(find_dotenv())

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]
client = WebClient(token=SLACK_BOT_TOKEN)

# Initialize apps
app = App(token=SLACK_BOT_TOKEN)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def get_workspace_owner_id():
    try:
        response = client.users_list()
        return next((m["id"] for m in response["members"] if m.get("is_owner")), None)
    except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return None

def get_channel_owner_id(channel_id):
    try:
        return client.conversations_info(channel=channel_id)["channel"].get("creator")
    except SlackApiError as e:
        print(f"Error fetching channel info: {e.response['error']}")
        return None

def is_user_admin(user_id):
    try:
        return client.users_info(user=user_id)["user"]["is_admin"]
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return False

def GetAllUsers():
    try:
        return {m['id']: m['profile']['real_name'] for m in client.users_list()["members"]}
    except SlackApiError as e:
        print(f"Error fetching users: {e.response['error']}")
        return {}

def get_slack_id_from_name(name):
    all_users = GetAllUsers()
    return next((uid for uid, uname in all_users.items() if uname.lower() == name.lower()), None)

def get_user_timezone(user_id):
    """Get user's timezone from Slack profile"""
    try:
        response = client.users_info(user=user_id)
        return response["user"]["tz"] or "UTC"
    except SlackApiError as e:
        print(f"Timezone error: {e.response['error']}")
        return "UTC"

all_users = GetAllUsers()

def extract_mentioned_users(text):
    return re.findall(r"<@(\w+)>", text)

@app.event("app_mention")
def handle_mentions(body, say):
    event = body["event"]
    user_id = event["user"]
    channel_id = event["channel"]
    text = event.get("text", "").replace(f"<@{SLACK_BOT_USER_ID}>", "").strip()

    # Authorization check
    workspace_owner = get_workspace_owner_id()
    channel_owner = get_channel_owner_id(channel_id)
    if user_id not in [workspace_owner, channel_owner] and not is_user_admin(user_id):
        say("Sorry, only workspace/channel owners or admins can mention this bot.")
        return

    # Get timezone and admin list
    timezone = get_user_timezone(user_id)
    admin_ids = ", ".join(uid for uid in all_users if is_user_admin(uid))
    
    say("On it! ⚡")
    
    response = agent_exec.invoke({
        'input': f"<@{user_id}> mentioned me: '{text}'",
        'event_details': event_details,
        'admin': admin_ids,
        'user_id': user_id,
        'target_user_id': None,
        'all_users': str(all_users),
        'timezone': timezone,
    })
    say(response['output'])

@app.event("message")
def handle_messages(body, say):
    event = body["event"]
    channel_type = event["channel_type"]
    user_id = event["user"]
    text = event.get("text", "").strip()
    channel_id = event["channel"]

    if user_id == SLACK_BOT_USER_ID:
        return

    # Get conversation history
    # try:
    #     # history = client.conversations_history(
    #     #     channel=channel_id,
    #     #     limit=10,
    #     #     inclusive=False
    #     # ).get("messages", [])[::-1]  # Reverse to chronological order
    #     # print(history)
    #     # # extracted_messages = []
    #     # extracted_titles = [
    #     #     msg.get("assistant_app_thread", {}).get("title", "").strip()
    #     #     for msg in history
    #     #     if msg.get("assistant_app_thread", {}).get("title")
    #     # ]

    #     # print(str(extracted_titles))
        
        
    # except SlackApiError as e:
    #     print(f"History error: {e.response['error']}")
    #     history_context = []

    mentioned_users = extract_mentioned_users(text)
    timezone = get_user_timezone(user_id)

    # Base agent parameters
    agent_params = {
        'input': f"{text}",
        'event_details': event_details,
        'user_id': user_id,
        'all_users': str(all_users),
        'admin': 'false',
        'target_user_id': None,
        'timezone': timezone,
    }

    if mentioned_users:
        for target_id in mentioned_users:
            if not is_user_admin(target_id):
                say(f"Sorry, I can't access <@{target_id}>'s schedule.")
                continue

            target_tz = get_user_timezone(target_id)
            say(f"⚡ Scheduling with <@{target_id}>...")
            
            response = agent_exec.invoke({
                **agent_params,
                'admin': target_id,
                'target_user_id': target_id,
                'timezone': target_tz,
                'input': f"Schedule with <@{target_id}>: {text}"
            })
            say(response['output'])
    else:
        response = agent_exec.invoke(agent_params)
        say(response['output'])

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run()