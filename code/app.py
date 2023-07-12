import os
import requests
import time
import base64


# Function to load environment variables from .env file
def load_env_vars(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    for line in lines:
        key, value = line.strip().split("=")
        os.environ[key] = value

# Get the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
load_env_vars(os.path.join(script_directory, ".env"))


# Get environment variables
IFTTT_KEY = os.getenv("IFTTT_KEY")
TOGGL_API_TOKEN = os.getenv("TOGGL_API_TOKEN")

def has_key_value_pair(json_object, key, value):
    return key in json_object and json_object[key] == value

def is_timer_running():
    auth_token = base64.b64encode(f"{TOGGL_API_TOKEN}:api_token".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.track.toggl.com/api/v8/time_entries/current", headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Toggl API request failed with status code {response.status_code}")
        return False
    return response.json()["data"]

def send_ifttt_request(event_name):
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{IFTTT_KEY}"
    response = requests.post(url)

    if response.status_code != 200:
        print(f"Error: IFTTT API request failed with status code {response.status_code}")
        return False

timer_running = False
send_ifttt_request("brave_off")

while True:
    toggl_timer_running = is_timer_running()
    if (toggl_timer_running is not None) and not timer_running:
        #if has_key_value_pair(toggl_timer_running, "pid", 172073056):
        #    send_ifttt_request("meeting_active")
        #else:
        send_ifttt_request("brave_on")
        timer_running = True
    elif not (toggl_timer_running is not None)  and timer_running:
        send_ifttt_request("brave_off")
        timer_running = False

    time.sleep(60)  # Check every minute