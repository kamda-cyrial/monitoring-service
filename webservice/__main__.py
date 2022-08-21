import os
from prestige_cli import *
import asyncio
import os
import aiohttp
from aiohttp import web
from gidgethub.aiohttp import GitHubAPI
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from aiohttp import web

routes = web.RouteTableDef()

router = routing.Router()

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! You will be rewarded with Prestige XP if the issue is stamped with the approved_issue label. (I'm a bot!)."
    await gh.post(url, data={"body": message})

@router.register("issues", action="labeled")
async def issue_is_labeled(event, gh, *args, **kwargs):
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]
    label = event.data['label']['name']
    print("label issue called")
    print(f"Author: {author}, Label: {label}")
    if label == "approved_issue":
        print("condition met")
        amount = 3
        message = f"Recorded.  @{author} Will be rewarded with some Prestige XP(I'm a bot!)."
        reward_user(author, amount)
        await gh.post(url, data={"body": message})

@router.register("pull_requests", action="closed")
async def pull_request_closed(event, gh, *args, **kwargs):

    url = event.data["issue"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]
    merge_status = event.data["merged"]
    if merge_status:
        amount = 30
        message = f"Recorded.  @{author} Will be rewarded with some Prestige XP(I'm a bot!)."
        reward_user(author, amount)
        await gh.post(url, data={"body": message})


@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()
    gitdets = github_api_key()
    # our authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    # instead of mariatta, use your own username
    async with aiohttp.ClientSession() as session:
        
        gh = GitHubAPI(session, gitdets.user_name, oauth_token=oauth_token)
        print("event did get called, just logging")
        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)