import requests
from datetime import datetime, timedelta

# GitHub API base URL
BASE_URL = "https://api.github.com"

def get_pull_requests(owner, repo):
    # Construct the URL to get pull requests
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"

    # Set up parameters to filter pull requests by date
    since_date = (datetime.now() - timedelta(days=7)).isoformat()
    params = {"state": "all", "since": since_date}

    # Make a GET request to the GitHub API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch pull requests. Status code: {response.status_code}")

def generate_email_summary(owner, repo, pull_requests):
    # Prepare email details
    from_email = "your_email@example.com"
    to_email = "recipient_email@example.com"
    subject = f"GitHub Pull Request Summary - {owner}/{repo}"

    # Prepare the body of the email
    body = f"Hello,\n\nHere is the summary of pull requests for the last week in the {owner}/{repo} repository:\n\n"

    for pr in pull_requests:
        state = pr["state"]
        title = pr["title"]
        user = pr["user"]["login"]
        created_at = pr["created_at"]
        merged_at = pr.get("merged_at", "Not Merged")

        body += f" - {state.capitalize()}: {title} (by {user}) - Created at {created_at}, Merged at {merged_at}\n"

    # Add a closing note
    body += "\nBest regards,\nYour Name"

    return from_email, to_email, subject, body

if __name__ == "__main__":
    # Replace these values with the target repository details
    owner = "owner_username"
    repo = "repository_name"

    # Get pull requests from the last week
    pull_requests = get_pull_requests(owner, repo)

    # Generate email summary
    from_email, to_email, subject, body = generate_email_summary(owner, repo, pull_requests)

    # Print the details of the email
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("\nBody:\n")
    print(body)