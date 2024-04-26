from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from colorama import Fore , Style , Back
from hexer import mHash
from datetime import datetime
import threading
import mnemonic


def timer() :
    tcx = datetime.now().time()
    return tcx

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

p2shp = """
                                 ---***---
           
           ███╗    ██████╗ ██████╗ ██████╗ ██╗  ██╗██╗  ██╗    ███╗
           ██╔╝    ██╔══██╗╚════██╗██╔══██╗██║ ██╔╝██║  ██║    ╚██║
           ██║     ██████╔╝ █████╔╝██████╔╝█████╔╝ ███████║     ██║
           ██║     ██╔═══╝ ██╔═══╝ ██╔═══╝ ██╔═██╗ ██╔══██║     ██║
           ███╗    ██║     ███████╗██║     ██║  ██╗██║  ██║    ███║
           ╚══╝    ╚═╝     ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══╝
                                                                   
                                 ---***---                                         
        """

print(Fore.YELLOW + p2shp)

filename = 'P2PKH.txt'
with open(filename) as f :
    add = f.read().split()
add = set(add)
print(Fore.WHITE , '[*]All Address TYPE P2PKH Start With 1 import Now...' , Back.RED , timer() , Style.RESET_ALL , '\n')
print(
    Fore.BLUE + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~(' + Fore.YELLOW + ' M M D R Z A . C o M ' + Fore.BLUE + ')~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

r = 1
cores = 8

def seek(r) :
    z = 0
    w = 0
    while True :
        txx = timer()
        seed = generate_mnemonic()
        hdwallet: HDWallet = HDWallet(symbol = SYMBOL)
        hdwallet.from_mnemonic(mnemonic = seed)
        hdwallet.from_path(path="m/44'/0'/0'/0/0")
        addr = hdwallet.p2pkh_address()
        priv = hdwallet.private_key()

        print(Fore.GREEN , 'Total:' , Fore.YELLOW , str(z) , Fore.GREEN , 'Win:' , Fore.WHITE , str(w) , Fore.RED ,
              str(addr) , Back.MAGENTA , Fore.WHITE , txx , Style.RESET_ALL ,
              end = '\r')
        z += 1
        if addr in add :
            w += 1
            print(Fore.WHITE , 'Winning Wallet On Database File Imported ... [LOADED]')
            print(Fore.CYAN , 'All Details Saved On Text File Root Path ... [WRITED]')
            f = open("winner.txt" , "a")
            f.write('\n' , str(addr))
            f.write('\n' , str(seed))
            f.write('\n' , str(priv))
            f.write('\n==========[PROGRAMMER BY MMDRZA.CoM]==========\n')
            f.close()
            print(Fore.MAGENTA , 'Information File Name ========> p2shWinerWalletDetails.txt [OK]')
            continue


seek(r)

for i in range(cores):
    t = Thread(target = seek , args = r)
    t.start()
    t.join()
