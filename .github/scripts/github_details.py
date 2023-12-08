import requests
import os

def get_github_events(event_type):
    # Set up the variables
    github_repository = os.getenv('GITHUB_REPOSITORY')
    github_token = os.getenv('GITHUB_TOKEN')
    print (f"Github repository: {github_repository}")
    print (f"Github token: {github_token}")

    # Define the API endpoint
    api_url = f"https://api.github.com/repos/{github_repository}/events"

    # Set up headers for authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Print debug information
    print("API URL:", api_url)
    print("Headers:", headers)

    try:
        # Make the request
        response = requests.get(api_url, headers=headers)

        # Print raw response for debugging
        print("Raw Response:", response.text)

        # Check for successful response
        if response.status_code == 200:
            events = response.json()
            # Filter for specific event type (push or pull_request)
            filtered_events = [event for event in events if event['type'] == event_type]
            return filtered_events
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
push_events = get_github_events('PushEvent')
pull_events = get_github_events('PullRequestEvent')

print("Push Events:", push_events)
print("Pull Events:", pull_events)
