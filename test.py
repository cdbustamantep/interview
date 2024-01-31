import requests
from datetime import datetime, timedelta
BASE_URL = "https://api.github.com"
owner = "cdbustamantep"
repo = "interview"
# Construct the URL to get pull requests
url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
# Set up parameters to filter pull requests by date
since_date = (datetime.now() - timedelta(days=7)).isoformat()
params = {"state": "all", "since": since_date}

# Make a GET request to the GitHub API
response = requests.get(url, params=params)
response.json()
print (url)
print(response.text)