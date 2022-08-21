from urllib import request
import click
from state import keypair_from_json, github_api_key
import processor
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from borsh_construct import *

client = Client("https://api.devnet.solana.com")

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

entry.add_command(init_configs)
entry.add_command(register)
entry.add_command(reward_user)
if __name__ == '__main__':
    entry()