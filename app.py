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




## use of llm object
q = Query()
q.system_prompt = "Help User with ans"
q.prompt = "say hello"

llm = OpenAILLM(
    model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    base_url="https://api.together.xyz",
    api_key="3c98137bd32351482bbd172add8248e6c5918d1e94e882f2f5fcd3d8bfa6a839"
)

llm(q)

print(q.response)

USER_PROMPT_DIFF_SUMMARIZATION="""
You are a senior developer with deep buisness knowledge of you projects. 
You will be diff files from PRs, You job is to summarize each change that the PR brings at a function level, make sure to use bullet points and render in MARKDOWN Be as Descriptive as possible. Also higlight and make the summaries slightly buisness whenever possible.
"""

# ## sample diff review
# gdf = GitDiffReviewer("./")
# gdf.add(llm)
# gdf.user_prompt_query=USER_PROMPT_DIFF_SUMMARIZATION
# diff_string = get_diff_string("https://github.com/juspay/hyperswitch/pull/7508")
# res = gdf(diff_string)
# print(res.response)




app.post("/reviews")
async def review_pr(request: Request):
    request=request.json()
    gdf = GitDiffReviewer("./")
    gdf.user_prompt_query=USER_PROMPT_DIFF_SUMMARIZATION
    gdf.add(llm)
    diff_string = request.get("diff_string")
    res = gdf(diff_string)
    try:
        status=add_comment(llm_response=res.response,pr_number=request.pr_number)
        if status!=201:
            return {"status":"success","message":"Failed to add comments"},500
    except Exception as e:
        return {"status":"success","message":e},500
    return {"status":"success"},200