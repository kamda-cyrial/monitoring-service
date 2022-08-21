from urllib import request
import click
from state import keypair_from_json, github_api_key
import processor
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from borsh_construct import *
import asyncio
import os
import aiohttp
from aiohttp import web
from gidgethub.aiohttp import GitHubAPI
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

client = Client("https://api.devnet.solana.com")

routes = web.RouteTableDef()
router = routing.Router()

@click.group()
def entry():
    pass



@click.command(name = "register")
@click.argument("user_name")
@click.argument("wallet_address")
def register(user_name, wallet_address):
    payer_keypair = keypair_from_json("../deploy/authorizer_keypair.json")
    request = processor.process_register_user(payer_keypair, user_name, PublicKey(wallet_address), client)
    print("Transaction Id: ", request['result'])

@click.command(name="init")
def init_configs():
    payer_keypair = keypair_from_json("../deploy/authorizer_keypair.json")
    request = processor.process_init_configuration(payer_keypair, client)
    print("Transaction Id: ", request['result'])

@click.command(name="reward")
@click.argument("amount")
@click.argument("user_name")
def reward_user(user_name, amount):
    payer_keypair = keypair_from_json("../deploy/authorizer_keypair.json")
    request = processor.process_reward_xp(payer_keypair, user_name, int(amount), client)
    print("Transaction Id: ", request['result'])


@click.command(name="monitor")
def monitor():
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)

    loop.run_until_complete(start_monitor())
loop = asyncio.get_event_loop()

@routes.post("/")
async def start_monitor(link):
    gitdets = github_api_key()
    

    body = await request.read()

    # our authentication token and secret
    secret = os.environ.get(gitdets.secret_key)
    oauth_token = os.environ.get(gitdets.api_key)

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, gitdets.user_name, oauth_token=gitdets.api_key)
        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    return web.Response(status=200)



entry.add_command(init_configs)
entry.add_command(register)
entry.add_command(reward_user)
entry.add_command(monitor)
if __name__ == '__main__':
    entry()