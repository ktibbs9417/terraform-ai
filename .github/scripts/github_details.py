
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
    pr_number = event['payload']['number']
    changes = event.get('payload', {}).get('changes', {})
    title_from = changes.get('title', {}).get('from', 'N/A')
    body_from = changes.get('body', {}).get('from', 'N/A')
    pr_details = json.dumps(event['payload']['pull_request'], indent=4)
    reason = event['payload'].get('reason', 'N/A')
    return f"Pull Request Event:\nAction: {action}, Number: {pr_number}\nChanges: Title from {title_from}, Body from {body_from}\nPull Request Details:\n{pr_details}\nReason: {reason}"

def format_push_event(event):
    """
    Format a Push event for sending as a message.

    Parameters:
    event (dict): The event data from GitHub.

    Returns:
    str: Formatted message string.
    """
    ref = event['payload']['ref']
    num_commits = len(event['payload']['commits'])
    commits_details = []
    for commit in event['payload']['commits']:
        commit_message = commit['message']
        commit_author = commit['author']['name']
        commit_url = commit['url']
        commits_details.append(f"Message: {commit_message}, Author: {commit_author}, URL: {commit_url}")
    commits_info = "\n".join(commits_details)
    return f"Push Event to {ref}, Total Commits: {num_commits}\nCommits Details:\n{commits_info}"

def process_github_events(events, event_type):
    """
    Process GitHub events, filtering and formatting messages based on event type.

    Parameters:
    events (list): List of events from GitHub.
    event_type (str): Type of event to filter (e.g., 'PushEvent', 'PullRequestEvent').

    Returns:
    list: List of formatted message strings.
    """
    messages = []
    for event in events:
        if event['type'] == 'PullRequestEvent' and event_type == 'PullRequestEvent':
            messages.append(format_pull_request_event(event))
        elif event['type'] == 'PushEvent' and event_type == 'PushEvent':
            messages.append(format_push_event(event))
    return messages

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
        if response.status_code == 200:
            events = response.json()
            return process_github_events(events, event_type)
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    google_chat_webhook_url = os.getenv('GOOGLE_CHAT_WEBHOOK_URL')
    event_type = os.getenv('GITHUB_EVENT_TYPE')  # Event type from environment variable

    # Check if the event type is either 'PushEvent' or 'PullRequestEvent'
    if event_type in ['PushEvent', 'PullRequestEvent']:
        events_messages = get_github_events(event_type)

        # Only send a message if there are events to report
        if events_messages:
            message = f"GitHub {event_type}:\n" + "\n".join(events_messages)
            send_to_google_chat(google_chat_webhook_url, message)
        else:
            print(f"No events found for {event_type}")
    else:
        print(f"Invalid or unspecified event type: {event_type}")