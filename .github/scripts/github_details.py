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

def main():
    token = os.getenv('GITHUB_TOKEN')  # Replace with your GitHub token
    repo = os.getenv('GITHUB_REPOSITORY')  # Repository name in the format 'owner/repo'
    event = os.getenv('GITHUB_EVENT_NAME')

    if event == 'pull_request':
        pull_number = os.getenv('GITHUB_REF')
        details = get_pull_request_details(repo, pull_number, token)
        # Process the pull request details here

    elif event == 'push':
        commit_sha = os.getenv('GITHUB_SHA')
        details = get_commit_details(repo, commit_sha, token)
        # Process the commit details here

    # Convert details to a string or format as needed
    message = json.dumps(details, indent=4)
    print(message)

if __name__ == "__main__":
    main()