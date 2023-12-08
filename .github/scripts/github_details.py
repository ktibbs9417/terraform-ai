
import requests
import os
import json

def send_to_google_chat(webhook_url, message):
    """
    Send a message to a Google Chat room using a webhook.

    Parameters:
    webhook_url (str): The URL of the webhook for the Google Chat room.
    message (str): The message to be sent.

    Returns:
    None
    """
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data = {'text': message}
    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            print(f"Error sending message to Google Chat (Status code: {response.status_code})")
    except Exception as e:
        print(f"An error occurred while sending message to Google Chat: {e}")

def format_pull_request_event(event):
    """
    Format a Pull Request event for sending as a message.

    Parameters:
    event (dict): The event data from GitHub.

    Returns:
    str: Formatted message string.
    """
    action = event['payload']['action']
    pr_number = event['payload']['pull_request']['number']
    pr_changes = event['payload'].get('changes', {})
    title_from = pr_changes.get('title', {}).get('from', 'N/A')
    body_from = pr_changes.get('body', {}).get('from', 'N/A')
    pr_details = json.dumps(event['payload']['pull_request'], indent=4)

    formatted_message = (
        f"PullRequestEvent Action: {action}, Number: {pr_number}\n"
        f"Title Changed From: {title_from}\n"
        f"Body Changed From: {body_from}\n"
        f"Pull Request Details: {pr_details}"
    )
    print(f"Formatted PullRequestEvent Message Type: {type(formatted_message)}")

    return str(formatted_message)
def format_push_event(event):
    """
    Format a Push event for sending as a message.

    Parameters:
    event (dict): The event data from GitHub.

    Returns:
    str: Formatted message string.
    """
    # Extracting relevant details from the event
    event_id = event['id']
    event_type = event['type']
    actor = event['actor']['login']
    repo_name = event['repo']['name']
    commits = event['payload']['commits']
    is_public = event['public']
    created_at = event['created_at']

    # Formatting commit details
    commit_messages = [f"{commit['author']['name']}: {commit['message']}" for commit in commits]

    # Creating the formatted message
    formatted_message = (
        f"GitHub PushEvent:\n"
        f"ID: {event_id}\n"
        f"Type: {event_type}\n"
        f"Actor: {actor}\n"
        f"Repository: {repo_name}\n"
        f"Commits:\n" + "\n".join(commit_messages) + "\n"
        f"Public: {is_public}\n"
        f"Created at: {created_at}"
    )
    print(f"Formatted PushEvent Message Type: {type(formatted_message)}")
    return formatted_message

def process_github_events(event, event_type):
    """
    Process GitHub events, filtering and formatting messages based on event type.

    Parameters:
    events (list): List of events from GitHub.
    event_type (str): Type of event to filter (e.g., 'PushEvent', 'PullRequestEvent').

    Returns:
    list: List of formatted message strings.
    """
    if event_type == 'PushEvent':
        return format_push_event(event)
    elif event_type == 'PullRequestEvent':
        return format_pull_request_event(event)
    # Add other event types if needed
    else:
        return "Unsupported event type"

def get_github_events(event_type):
    """
    Fetch and process events from a GitHub repository.

    Parameters:
    event_type (str): The type of GitHub event to fetch (e.g., 'PushEvent', 'PullRequestEvent').

    Returns:
    list: List of filtered and formatted GitHub events.
    """
    github_repository = os.getenv('GITHUB_REPOSITORY')
    github_token = os.getenv('GITHUB_TOKEN')
    api_url = f"https://api.github.com/repos/{github_repository}/events"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {github_token}'
    }
    try:
        response = requests.get(api_url, headers=headers)
        #print(f"GitHub API Response: {response.status_code}, {response.text}")  # Log the raw response
        if response.status_code == 200:
            events = response.json()
            if events and events[0]['type'] == event_type:
                return events[0]
            return []
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    google_chat_webhook_url = os.getenv('GOOGLE_CHAT_WEBHOOK')
    event_type = os.getenv('GITHUB_EVENT_TYPE')  # Event type from environment variable

    print(f"Event Type: {event_type}")
    event = get_github_events(event_type)
    if event and event['type'] == 'PushEvent':
        print("Processing PushEvent")
        message = format_push_event(event)
        send_to_google_chat(google_chat_webhook_url, message)
    else:
            print("Error: Non-string elements found in events_messages")
