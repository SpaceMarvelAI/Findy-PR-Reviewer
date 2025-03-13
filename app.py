# 
import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from utils.diff_utils import get_diff_string,add_comment
from jaf.core.llm.openai import OpenAILLM
from jaf.types import Query
from jaf.pipeline.code.git_diff_reviewer import GitDiffReviewer
app=FastAPI()
load_dotenv("/.env")

print("Starting application...")


## use of llm object
q = Query()
q.system_prompt = "Help User with ans"
q.prompt = "say hello"

print("Initializing LLM...")
llm = OpenAILLM(
    model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    base_url="https://api.together.xyz",
    api_key="3c98137bd32351482bbd172add8248e6c5918d1e94e882f2f5fcd3d8bfa6a839"
)

print("Calling LLM for initial test...")
llm(q)


print(f"LLM Response: {q.response}")
print(f"LLM Prompt: {q.prompt}")

USER_PROMPT_DIFF_SUMMARIZATION="""
You are a senior developer with deep buisness knowledge of you projects. 
You will be diff files from PRs, You job is to summarize each change that the PR brings at a function level, make sure to use bullet points and render in MARKDOWN Be as Descriptive as possible. Also higlight and make the summaries slightly buisness whenever possible.
"""

print("User prompt for diff summarization defined")

# ## sample diff review
# gdf = GitDiffReviewer("./")
# gdf.add(llm)
# gdf.user_prompt_query=USER_PROMPT_DIFF_SUMMARIZATION
# diff_string = get_diff_string("https://github.com/juspay/hyperswitch/pull/7508")
# res = gdf(diff_string)
# print(res.response)


@app.post("/reviews")
async def review_pr(request: Request):
    print(f"Received review request")
    request_json = await request.json()
    print(f"Request JSON: {request_json}")
    
    print("Initializing GitDiffReviewer...")
    gdf = GitDiffReviewer("./")
    gdf.user_prompt_query=USER_PROMPT_DIFF_SUMMARIZATION
    gdf.add(llm)
    
    diff_string = request_json.get("diff_string")
    pr_number = request_json.get("pr_number")
    print(f"PR Number: {pr_number}")
    print(f"Diff string length: {len(diff_string) if diff_string else 0}")
    
    print("Calling GitDiffReviewer...")
    res = gdf(diff_string)
    print(f"GitDiffReviewer response received, length: {len(res.response) if res.response else 0}")
    
    try:
        print("Adding comment to PR...")
        status=add_comment(llm_response=res.response, pr_number=pr_number)
        print(f"Comment status code: {status}")
        if status!=201:
            print(f"Failed to add comment, status code: {status}")
            return {"status":"error","message":"Failed to add comments"}, 500
    except Exception as e:
        print(f"Exception when adding comment: {str(e)}")
        return {"status":"error","message":str(e)}, 500
    
    print("Successfully completed PR review")
    return {"status":"success"}, 200