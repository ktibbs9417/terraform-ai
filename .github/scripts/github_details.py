import os
import requests
import json

def get_pull_request_details(repo, pull_number, token):
    """
    Fetch details of a specific pull request.
    """
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_number}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_commit_details(repo, commit_sha, token):
    """
    Fetch details of a specific commit.
    """
    url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def create_message(commit_data):
    author_name = commit_data.get('author', {}).get('name', 'Unknown Author')
    commit_message = commit_data.get('message', 'No commit message')
    message = f"New commit by {author_name}: {commit_message}"
    return message


def main():
    webhook_url = os.getenv('GOOGLE_CHAT_WEBHOOK')
    commit_data = {} # Replace this with your actual logic to get commit data

    print("Commit data:", commit_data)  # Debugging line
    message = create_message(commit_data)
    payload = {"text": message}

    response = requests.post(webhook_url, json=payload)
    print(response.text)

if __name__ == "__main__":
    main()