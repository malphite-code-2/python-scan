from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from colorama import Fore , Style , Back
from hexer import mHash
from datetime import datetime
import threading

def timer() :
    tcx = datetime.now().time()
    return tcx


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

print(p2shp)

filename = 'P2PKH.txt'
with open(filename) as f :
    add = f.read().split()
add = set(add)
print('[*]All Address TYPE P2SH+P2WSH Start With 1 import Now...' , timer() , '\n')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~(M M D R Z A . C o M)~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

r = 1
cores = 4

def seek(r) :
    z = 0
    w = 0
    while True :
        txx = timer()
        hdwallet: HDWallet = HDWallet(symbol = SYMBOL)
        hdwallet.from_private_key(private_key = mHash())
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
            f.write('\n' , str(priv))
            f.write('\n==========[PROGRAMMER BY MMDRZA.CoM]==========\n')
            f.close()
            print(Fore.MAGENTA , 'Information File Name ========> winner.txt [OK]')
            continue


seek(r)

for i in range(cores):
    t = Thread(target = seek , args = i)
    t.start()
    t.join()
