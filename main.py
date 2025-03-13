import requests
import json

# Define your GitHub credentials and repository details
GITHUB_TOKEN = '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'
REPO_OWNER = 'SpaceMarvelAI'
REPO_NAME = 'Findy-PR-Reviewer'
PR_NUMBER = '2'

# Define the comment you want to add
comment_body = 'Test comment via api'

# Set up the API request headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github+json'
}

# Construct the API URL for adding a comment
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{PR_NUMBER}/comments'

# Prepare the data for the POST request
data = {
    'body': comment_body
}

# Send the POST request to add the comment
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 201:
    print('Comment added successfully.')
else:
    print(f'Failed to add comment. Status code: {response.status_code}')
