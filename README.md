# PR Review Agent

A FastAPI application that provides automated code reviews for pull requests, designed to be triggered by GitHub Actions or webhooks. The agent analyzes PR diffs and adds line-level comments with actionable feedback.

## Features

- Automatically review pull requests when triggered by GitHub Actions or webhooks
- Add line-level comments directly to GitHub PRs
- Stream real-time updates during the review process
- Get detailed feedback including comments and suggestions
- Pydantic validation for request/response models
- Server-Sent Events (SSE) for real-time updates
- GitHub webhook integration

## How It Works

1. The agent receives a PR review request (via API or webhook)
2. It fetches the PR diff from GitHub
3. The diff is analyzed using an LLM (Llama 3.3 70B via Together.xyz)
4. Line-level comments are extracted from the LLM's response
5. Comments are posted to the GitHub PR using the GitHub API
6. The review status is updated and can be monitored via API

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```
# GitHub Authentication
GITHUB_TOKEN=your_github_token_here
GITHUB_APP_ID=your_github_app_id_here
GITHUB_APP_PRIVATE_KEY=your_github_app_private_key_here
GITHUB_WEBHOOK_SECRET=your_github_webhook_secret_here

# LLM API
TOGETHER_API_KEY=your_together_api_key_here
```

## Usage

### Start the server

```bash
cd pr-review-agent
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Manually Trigger a PR Review

You can manually trigger a PR review by making a POST request to the `/api/reviews` endpoint:

```bash
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "repository": {
      "owner": "username",
      "name": "repo-name",
      "url": "https://github.com/username/repo-name"
    },
    "pull_request": {
      "id": 123456,
      "number": 42,
      "title": "Add new feature",
      "description": "This PR adds a new feature",
      "branch": "feature/new-feature",
      "base_branch": "main",
      "url": "https://github.com/username/repo-name/pull/42"
    },
    "token": "github_token",
    "review_type": "standard"
  }'
```

## GitHub Actions Integration

### Setting up the GitHub Action

Create a `.github/workflows/pr-review.yml` file in your repository:

```yaml
name: PR Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger PR Review
        uses: actions/github-script@v6
        with:
          script: |
            const response = await fetch('https://your-pr-review-agent-url/api/github/webhook', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-GitHub-Event': 'pull_request'
              },
              body: JSON.stringify({
                action: context.payload.action,
                repository: context.payload.repository,
                pull_request: context.payload.pull_request,
                sender: context.payload.sender
              })
            });
            
            const result = await response.json();
            console.log('PR Review task created:', result);
```

## GitHub Webhook Integration

You can also set up a GitHub webhook to trigger reviews automatically:

1. Go to your repository settings
2. Navigate to Webhooks
3. Add a new webhook:
   - Payload URL: `https://your-pr-review-agent-url/api/github/webhook`
   - Content type: `application/json`
   - Secret: Your `GITHUB_WEBHOOK_SECRET` value
   - Events: Select "Pull requests"

## Customizing the Review Process

You can customize the review process by modifying the prompt in the `run_pr_review` function in `app.py`:

```python
gdf.what_to_do("""
Your custom review instructions here
""")
```

## Development

### Project Structure

- `app.py`: Main application file with FastAPI routes and review logic
- `.env`: Environment variables
- `requirements.txt`: Python dependencies

### Adding New Features

To extend the functionality:

1. Add new routes in `app.py`
2. Enhance the review logic in the `run_pr_review` function
3. Add new models as needed using Pydantic

## License

MIT 