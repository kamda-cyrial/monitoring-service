import json
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

label_dict = {
        "approved_issue": 30,
    }

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
    print(f"Author: {author}, Label: {label}, Url: {url}")
    if label in label_dict.keys():
        print("condition met")
        amount = int(label_dict[label]/10)
        message = f"Recorded.  @{author} Will be rewarded with some Prestige XP(I'm a bot!)."
        reward_user(author, amount)
        await gh.post(url, data={"body": message})


@router.register("pull_request", action="closed")
async def pull_request_closed(event, gh, *args, **kwargs):
    print(json.dumps(event.data, indent=4))
    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]
    merge_status = event.data["pull_request"]["merged"]
    labels = event.data["pull_request"]['labels']

    for key in label_dict.keys():
        if key in labels:
            print(f"url: {url}, author: {author}, merge status: {merge_status}")
            if merge_status:
                amount = 30
                message = f"Recorded.  @{author} Will be rewarded with some Prestige XP(I'm a bot!)."
                reward_user(author, amount)
                await gh.post(url, data={"body": message})
            break


@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()
    gitdets = github_api_key()
    # our authentication token and secret
    secret = gitdets.secret_key
    oauth_token = gitdets.api_key

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    # instead of mariatta, use your own username
    async with aiohttp.ClientSession() as session:
        
        gh = GitHubAPI(session, gitdets.user_name, oauth_token=oauth_token)
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