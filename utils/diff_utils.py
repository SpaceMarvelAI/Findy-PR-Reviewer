import requests
import json
def get_diff_string(repo_path:str):
    diff=requests.get(repo_path+".diff")
    return diff.text



def add_comment(llm_response:str,pr_number='1'):
    GITHUB_TOKEN = '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'
    REPO_OWNER = 'SpaceMarvelAI'
    REPO_NAME = 'Findy-PR-Reviewer'
    

    # Define the comment you want to add
    comment_body = llm_response
    # Set up the API request headers
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github+json'
    }

    # Construct the API URL for adding a comment
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments'

    # Prepare the data for the POST request
    data = {
        'body': comment_body
    }
    # Send the POST request to add the comment
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 201:
        print('Comment added successfully.')
        return response.status_code
    else:
       
        print(f'Failed to add comment. Status code: {response.status_code}')
        return response.status_code