import base64
import solana
from solana.publickey import PublicKey
from solana import system_program
from solana.transaction import *
from spl.token import constants as spl_constants
from spl.token import instructions as assoc_instructions
from instruction import *
from state import Constants as prestige_constants
from state import UserData

def process_init_configuration(payer_keypair, client):
    mint_account_key, mint_account_bump = PublicKey.find_program_address([bytes(prestige_constants.XP_MINT_KEY, 'utf-8')], prestige_constants.program_id)
    general_authority_address, general_authority_bump = PublicKey.find_program_address([bytes(prestige_constants.GENERAL_AUTHORITY_KEY, 'utf-8')], prestige_constants.program_id)
    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    mint_account_meta = AccountMeta(mint_account_key, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    general_authority_meta = AccountMeta(general_authority_address, False, False)
    sysvar_rent_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        mint_account_meta,
        spl_program_meta,
        general_authority_meta,
        sysvar_rent_meta,

        sys_program_meta,
        spl_program_meta,
    ]
    if(payer_keypair.public_key != prestige_constants.authorized_signer):
        print("Error: Couldn't certify signer as the authorized person")
        return
    data = build_instruction(InstructionEnum.enum.InitProgram())
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, prestige_constants.program_id, data))
    return client.send_transaction(transaction, payer_keypair)

def process_register_user(payer_keypair,user_name, user_address, client):
    mint_account_key, mint_account_bump = PublicKey.find_program_address([bytes(prestige_constants.XP_MINT_KEY, 'utf-8')], prestige_constants.program_id)
    user_token_address = assoc_instructions.get_associated_token_address(user_address, mint_account_key)
    general_authority_address, general_authority_bump = PublicKey.find_program_address([bytes(prestige_constants.GENERAL_AUTHORITY_KEY, 'utf-8')], prestige_constants.program_id)
    user_data_address, user_data_bump = PublicKey.find_program_address([bytes(prestige_constants. USERREGKEY, 'utf-8'), bytes(user_name, 'utf-8')], prestige_constants.program_id)
    
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    user_account_meta = AccountMeta(user_address, False, True)
    user_data_meta = AccountMeta(user_data_address, False, True)
    user_token_meta = AccountMeta(user_token_address, False, True)
    mint_account_meta = AccountMeta(mint_account_key, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    general_authority_meta = AccountMeta(general_authority_address, False, False)
    sysvar_rent_meta = AccountMeta(solana.sysvar.SYSVAR_RENT_PUBKEY, False, False)
    sys_program_meta = AccountMeta(system_program.SYS_PROGRAM_ID, False, False)
    associated_program_meta = AccountMeta(spl_constants.ASSOCIATED_TOKEN_PROGRAM_ID, False, False)


    accounts = [
        payer_account_meta,
        user_account_meta,
        user_data_meta,
        user_token_meta,
        mint_account_meta,
        sys_program_meta,
        spl_program_meta,
        general_authority_meta,

        sys_program_meta,
        associated_program_meta,
        spl_program_meta,
    ]
    if(payer_keypair.public_key != prestige_constants.authorized_signer):
        print("Error: Couldn't certify signer as the authorized person")
        return
    data = build_instruction(InstructionEnum.enum.RegisterUser(user_name= bytes(user_name, 'utf-8')))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, prestige_constants.program_id, data))
    return client.send_transaction(transaction, payer_keypair)

def process_reward_xp(payer_keypair,user_name, xp, client):
    mint_account_key, mint_account_bump = PublicKey.find_program_address([bytes(prestige_constants.XP_MINT_KEY, 'utf-8')], prestige_constants.program_id)
    general_authority_address, general_authority_bump = PublicKey.find_program_address([bytes(prestige_constants.GENERAL_AUTHORITY_KEY, 'utf-8')], prestige_constants.program_id)
    user_data_address, user_data_bump = PublicKey.find_program_address([bytes(prestige_constants. USERREGKEY, 'utf-8'), bytes(user_name, 'utf-8')], prestige_constants.program_id)

    user_address = PublicKey(UserData.parse(base64.urlsafe_b64decode(client.get_account_info(user_data_address)['result']['value']['data'][0])).user_address)

    user_token_address = assoc_instructions.get_associated_token_address(user_address, mint_account_key)
    print("user_address: ", user_address)
    payer_account_meta = AccountMeta(payer_keypair.public_key, True, True)
    user_account_meta = AccountMeta(user_address, False, True)
    user_data_meta = AccountMeta(user_data_address, False, True)
    user_token_meta = AccountMeta(user_token_address, False, True)
    mint_account_meta = AccountMeta(mint_account_key, False, True)
    spl_program_meta = AccountMeta(spl_constants.TOKEN_PROGRAM_ID, False, False)
    general_authority_meta = AccountMeta(general_authority_address, False, False)


    accounts = [
        payer_account_meta,
        user_account_meta,
        user_data_meta,
        user_token_meta,
        mint_account_meta,
        spl_program_meta,
        general_authority_meta,

        spl_program_meta,
        spl_program_meta,
        spl_program_meta,
    ]
    if(payer_keypair.public_key != prestige_constants.authorized_signer):
        print("Error: Couldn't certify signer as the authorized person")
        return
    data = build_instruction(InstructionEnum.enum.RewardXP(total_xp = xp, user_name= bytes(user_name, 'utf-8')))
    transaction = Transaction()
    transaction.add(TransactionInstruction(accounts, prestige_constants.program_id, data))
    return client.send_transaction(transaction, payer_keypair)
