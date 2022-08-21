from borsh_construct import *
from solana.publickey import PublicKey
import json
from solana.keypair import Keypair
import base58

def keypair_from_json(filepath):
    keypair = Keypair.from_secret_key(json.load(open(filepath)))
    return keypair

class Constants:
    program_id = PublicKey("9HUVdKeXEFJVBuLKeM8y6u8pT3q4gNTnDRoKD29G3Dn5")

    authorized_signer = PublicKey("cb8zdnsdLA9dwzf65LmMZ745Z1M8DYSZZht1CADeouZ")

    USERREGKEY = "Prestige Registration"
    XP_MINT_KEY = "Prestige Mint Key"
    GENERAL_AUTHORITY_KEY = "freeze_and_mint_authority Key"

    USERDATA_STRUCT_KEY = 138_734_492

Rank = Enum(
    "None",
    "Novice",
    "Scholar",
    "Developer",
    "Mentor",
    
    enum_name="Rank"
)

Issue = CStruct(
    "issued_xp" / U64,
    "issue_id" / Vec(U8),
)


UserData = CStruct(
    "struct_key" / U32,
    "user_address" / U8[32],
    "total_xp" / U64,
    "rank" / Rank,
    "registration_date" / U32,
    # "all_issues" / Vec(Issue), //account Space Too Expensive to have. Will need to rediscuss in the meeting
)

def github_api_key():
    gitfile = json.load(open("./deploy/github_api_key.json"))
    class gitdets:
        user_name = gitfile["user_name"]
        api_key = gitfile["api_key"]
        secret_key = gitfile["secret_key"]
    return gitdets