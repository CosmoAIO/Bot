from datetime import datetime
from pypresence import Presence
# from stores.currys_backend import Currys
from termcolor import colored
import time
import os
import time

logo = """
 ██████╗ ██████╗ ███████╗███╗   ███╗ ██████╗  █████╗ ██╗ ██████╗ 
██╔════╝██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔══██╗██║██╔═══██╗
██║     ██║   ██║███████╗██╔████╔██║██║   ██║███████║██║██║   ██║
██║     ██║   ██║╚════██║██║╚██╔╝██║██║   ██║██╔══██║██║██║   ██║
╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝██║  ██║██║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝
""" + colored("""-----------------------------------------------------------------
   CosmoAIO - Retail Beta Bot (Currently UK only) - Cooking EU
-----------------------------------------------------------------
""", "cyan")

siteList = ["Currys", "Ebuyer", "Scan", "Overclockers", "Exit"]
status_time = datetime.now().strftime("%X")

discordPresence = Presence("824754849102954527")


def authentication():
    os.system("title CosmoAIO - Authenticating...")
    print(f"[{status_time}] Checking Key")
    # add authentication process above welcome message
    time.sleep(.500)
    print(f"[{status_time}] Welcome Back - Version v0.0.1")
    return


def updater():  # api needed to the server/host to track latest verion?
    os.system("title CosmoAIO - Checking for updates...")
    print(f"[{status_time}] Checking for Updates")
    # input - update downlader & installer
    time.sleep(.500)
    print(f"[{status_time}] Bot is up to date")
    return


def main():
    discordPresence.connect()
    discordPresence.update(state="Version 0.0.1", details="Running CosmoAIO", large_image="logo", start=time.time())
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    authentication()
    time.sleep(.500)
    updater()
    time.sleep(.250)
    os.system("title CosmoAIO - Main Menu")

    print("")
    for i in range(0, len(siteList)):
        print(str(i) + " - ", siteList[i])
    print("")

    selection = int(input("Please select an option: "))
    # eval(siteList[selection]+"()")

    if selection == 0:  # Currys
        import stores.currys_backend
    elif selection == 1:  # Ebuyer
        print("1")
    elif selection == 2:  # Scan
        print("2")
    else:  # Exit
        quit


if __name__ == '__main__':
    os.system("title CosmoAIO")
    main()
