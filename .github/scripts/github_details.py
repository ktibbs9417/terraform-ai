import requests
import os
def fetch_push_events(repo, token):
    url = f"https://api.github.com/repos/{repo}/events"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        push_events = [event for event in events if event['type'] == 'PushEvent']
        return push_events
    else:
        return None

# Example usage
repo = os.getenv("GITHUB_REPOSITORY")  # Replace with your repository
token = os.getenv("GITHUB_TOKEN")   # Replace with your GitHub token
print(f"Repo: {repo}\n")
push_events = fetch_push_events(repo, token)
print(push_events)

def fetch_pull_requests(repo, token):
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
pull_requests = fetch_pull_requests(repo, token)
print(pull_requests)