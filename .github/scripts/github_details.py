
import requests
import os
import json
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

        

def get_llm():
        return GooglePalm(temperature=0.0)

    
def ask(message, event_type):

        llm = get_llm()
        if event_type == 'PushEvent':
            template = '''
            You are a helpful assistant that is a Git Expert. Your goal is to provide detailed descriptions over PushEvents and PullRequestEvents that are triggered on GitHub.
            Provide a natural language response to the following GitHub Action that was taken place.
            Include details about the commit ID, the type of event, the actor, the repository name, commit messages, the date, and a link to the commit branch:

            GitHub Action: {message}
            '''
        elif event_type == 'PullRequestEvent':
            template = '''
            You are a helpful assistant that is a Git Expert. Your goal is to provide detailed descriptions over PushEvents and PullRequestEvents that are triggered on GitHub.
            Provide a natural language response to the following GitHub Action that was taken place.
            Include details about the Pull Request Action, the Pull Request Number, the Title Changed From, the Body Changed From, and the Pull Request Details:

            GitHub Action: {message}
            '''
        prompt = PromptTemplate(
                input_variables=["message"],
                template=template,
        )
        formatted = prompt.format(message=message)
        #print (f"Formatted message: {formatted}")
        print(f"Generating a natural language reponse to the GitHub Action\n")
        chain = LLMChain(
             llm = llm, 
             prompt = prompt
             )
        response = chain.run(formatted)
        print(f"Natural language response: {response}\n")
        # runnable = prompt | llm | StrOutputParser()
        # for chunk in runnable.stream({"message": "{message}"}):
        #     print(chunk, end="", flush=True)
        #print(f"Conversation chain: {conversation_chain}\n")
        return response

def send_to_google_chat(webhook_url, ai_message):
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
    data = {'text': ai_message}
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
    pr = event['payload']['pull_request']
    html_url = pr['html_url']
    title = pr['title']
    user_login = pr['user']['login']
    body = pr['body'] or "No body content"
    created_at = pr['created_at']
    assignee = pr['assignee']['login'] if pr['assignee'] else "No assignee"
    assignees = ", ".join([assignee['login'] for assignee in pr['assignees']])
    requested_reviewers = ", ".join([reviewer['login'] for reviewer in pr['requested_reviewers']])
    requested_teams = ", ".join([team['name'] for team in pr['requested_teams']])
    labels = ", ".join([label['name'] for label in pr['labels']])
    branch = pr['head']['label']
    mergeable = pr['mergeable']
    mergeable_state = pr['mergeable_state']
    additions = pr['additions']
    deletions = pr['deletions']
    changed_files = pr['changed_files']

    formatted_message = (
        f"Pull Request Event - {action}\n"
        f"URL: {html_url}\n"
        f"Title: {title}\n"
        f"Initiated by: {user_login}\n"
        f"Body: {body}\n"
        f"Created at: {created_at}\n"
        f"Assignee: {assignee}\n"
        f"Assignees: {assignees}\n"
        f"Requested Reviewers: {requested_reviewers}\n"
        f"Requested Teams: {requested_teams}\n"
        f"Labels: {labels}\n"
        f"From Branch: {branch}\n"
        f"Mergeable: {mergeable}\n"
        f"Mergeable State: {mergeable_state}\n"
        f"Additions: {additions}, Deletions: {deletions}, Changed Files: {changed_files}"
    )

    return formatted_message
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
    commit_messages = [f"{commit['author']['name']}: {commit['message']}: {commit['url']}" for commit in commits]

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
        #print(f"PushEvent Message: {message}")
        ai_message = ask(message, event_type)
        #print(f"AI Message: {ai_message}")
        send_to_google_chat(google_chat_webhook_url, ai_message)
    elif event and event['type'] == 'PullRequestEvent':
        print("Processing PullRequestEvent")
        message = format_pull_request_event(event)
        ai_message = ask(message, event_type)
        send_to_google_chat(google_chat_webhook_url, ai_message)
    else:
            print("Error: Non-string elements found in events_messages")
