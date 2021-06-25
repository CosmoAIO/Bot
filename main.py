from datetime import datetime
from pypresence import Presence
from modules.currys_backend import Currys
import time
import os
import time

logo = """
██╗   ██╗███╗   ██╗██╗████████╗███████╗ █████╗ ██╗ ██████╗ 
██║   ██║████╗  ██║██║╚══██╔══╝██╔════╝██╔══██╗██║██╔═══██╗
██║   ██║██╔██╗ ██║██║   ██║   █████╗  ███████║██║██║   ██║
██║   ██║██║╚██╗██║██║   ██║   ██╔══╝  ██╔══██║██║██║   ██║
╚██████╔╝██║ ╚████║██║   ██║   ███████╗██║  ██║██║╚██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ 

"""

siteList = ["Currys", "Ebuyer", "Scan", "Overclockers", "Exit"]
status_time = datetime.now().strftime("%X")

discordPresence = Presence("824754849102954527")


def authentication():
    os.system("title UniteAIO - Authenticating...")
    print(f"[{status_time}] Checking Key")
    # add authentication process above welcome message
    time.sleep(.500)
    print(f"[{status_time}] Welcome Back - Version v0.0.1")
    return


def updater():  # api needed to the server/host to track latest verion?
    os.system("title UniteAIO - Checking for updates...")
    print(f"[{status_time}] Checking for Updates")
    # input - update downlader & installer
    time.sleep(.500)
    print(f"[{status_time}] Bot is up to date")
    return


def main():
    discordPresence.connect()
    discordPresence.update(state="Version 0.0.1", details="Running UniteAIO", large_image="logo", start=time.time())
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    authentication()
    time.sleep(.500)
    updater()
    time.sleep(.250)
    os.system("title UniteAIO - Main Menu")

    print("")
    for i in range(0, len(siteList)):
        print(str(i) + " - ", siteList[i])
    print("")

    selection = int(input("Please select an option: "))
    eval(siteList[selection]+"()")

    if selection == 0:  # Currys
        Currys.main()
    elif selection == 1:  # Ebuyer
        scan.main()
    elif selection == 2:  # Scan
        overclockers.main()
    else:  # Exit
        quit


if __name__ == '__main__':
    os.system("title UniteAIO")
    main()
