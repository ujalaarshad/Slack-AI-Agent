import os
from dotenv import load_dotenv
from slack_sdk import WebClient

# Load environment variables
load_dotenv()

# Slack credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)
