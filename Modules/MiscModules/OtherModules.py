from names_generator import generate_name
from colorama import Fore
import datetime
import aiohttp
import asyncio
import sys
import os

cwd = os.getcwd()
parent_dtr = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(parent_dtr)
from Hydra import Hydra
from Modules import TextAssets

dnow = datetime.datetime.now().strftime("%H:%M:%S")

class OtherModules(TextAssets.AsciiAssets):
    """Misc Modules for discord, I made up for fun or they didnt fit in the other categories"""
    async def invite_info(self):
        os.system("cls")
        super().send_logo()
        self.cmessage("\n| Server invite >>: ",True)
        invite = input()
        finvite = invite.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/invites/{finvite}") as response:
                if response.status == 200:
                    data = await response.json()
                    security_level = data['guild']['verification_level']
                    guild_id = data['guild']['id']
                    inviter = data.get('inviter', {})
                    self.cmessage(f"\n| Server Data >>> {data['guild']['name']} ({guild_id})")
                    self.cmessage(f"| Server Description >>> {data['guild']['description']}.\n")
                    match security_level:
                        case 0:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (No Protection!)")
                        case 1:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required!)")
                        case 2:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 5 minutes!)")
                        case 3:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 10 minutes!)")
                        case 4:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 5 minutes! + Verified Phone Number!)")                    
                        case _:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Unknown)")
                    if inviter:
                        self.cmessage(f"| Inviter ~~> {data['inviter']['username']} ({data['inviter']['id']})")
                    else:
                         self.cmessage(f"| Inviter ~~> Vanity Invite ({finvite})")
                    if "AUTO_MODERATION" in data['guild']['features']:
                        self.cmessage("| AutoMod 🤖 ~~> ",True)
                        print(Fore.GREEN + "True")
                    else:
                        self.cmessage("| AutoMod 🤖 ~~> ",True)
                        print(Fore.RED + "False")
                    go_menu = input()
                    await Hydra.main.menu() 
                else:
                    self.cmessage("\nInvalid Discord link, the correct format is Ex.'https://discord.gg/g4eaH7EQJq'.")
                    exit = input()
                    await Hydra.main.menu() 
    
    async def dms_menu(self):
        os.system("cls")
        self.send_logo()
        self.cmessage("| Message >>: ",True)
        self.message = input()
        self.cmessage("| Channel ID >>: ",True)
        self.channel_id = input()
        self.cmessage("| User Token >>: ",True)
        self.user_token = input()
        self.cmessage("| Spammer Threads >>: ",True)
        self.threads = input()
        print()
        
        async def dm_spammer(self,message,token,channel_id):
            headers = {
                 "Authorization" : token
                }
            async with aiohttp.ClientSession() as session:
                 while True:
                        async with session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages",headers=headers,json={"content" : message}) as response:
                            match response.status:
                                case 200:
                                    print(Fore.GREEN + "| [Sent] ",end="")
                                    self.cmessage(f">>> {message} - {dnow}")
                                case 429:
                                    print(Fore.YELLOW + "| [Ratelimited] ",end="")
                                    self.cmessage(f">>> {message} - {dnow}")
                                case _:
                                    print(Fore.RED + "| [Ratelimited] ",end="")

        tasks = []
        for _ in range(int(self.threads)):
            tasks.append(dm_spammer(self,self.message,self.user_token,self.channel_id))
        await asyncio.gather(*tasks)
 

    async def gcnamechanger(self):
        os.system("cls")
        self.send_logo()
        self.cmessage("""
| [1] - Automatic
| [2] - Delay Based
|
| Option >>: """,True)
        option = input()
        self.cmessage("\n| Group Chat Channel ID >>: ",True)
        self.channel_id = input()
        self.cmessage("| User Token >>: ",True)
        self.token = input()
        if option == "2":
            self.cmessage("| Delay >>: ",True)
            delay = input()
        super().log(f"{dnow} | Group Name Changer Spammer >> Channel ID : {self.channel_id}")
        print()

        self.headers = {
            "Origin" : "https://canary.discord.com",
            "authorization" : self.token,
            "Content-Type" : "application/json"
        }
        tchanged = 0

        async def gcsp(self,channel_id):
            try:
                random_name = generate_name()
                async with aiohttp.ClientSession() as session:
                    async with session.patch(url=f"https://discord.com/api/v9/channels/{channel_id}",headers=self.headers, json={"name": random_name}) as response:
                        match response.status:
                            case 200:
                                print(Fore.GREEN + "[Changed Name] ",end="")
                                self.cmessage(f">>> '{random_name}' | {dnow}")
                            case 429:
                                print(Fore.YELLOW + "[Ratelimited] ",end="")
                                self.cmessage(f">>> '{random_name}' | {dnow}")
                            case _:
                                self.cmessage(f"[Failed] Failed to Spam URL: {response.status}")
            except Exception as e:
                self.cmessage(f"[ERROR] Failed to Spam URL: {str(e)}")
            except KeyboardInterrupt:
                await asyncio.sleep(3)
                await Hydra.main.menu()
    
        tasks = []
        while True:
            try:
                if option == "1":
                    for _ in range(5):
                        task = asyncio.create_task(gcsp(self.channel_id))
                        tasks.append(task)
                        tchanged += 1
                    match tchanged / 5:
                        case 1:
                            await asyncio.sleep(3)
                        case 2:
                            await asyncio.sleep(9)
                        case 3:
                            await asyncio.sleep(4)
                        case _:
                            tchanged = 5
                            await asyncio.sleep(7)
                    await asyncio.gather(*tasks)
                    continue
                else:
                    for _ in range(1):
                        await gcsp(self.channel_id)
                        await asyncio.sleep(float(delay))
                        continue
            except KeyboardInterrupt:
                await asyncio.sleep(3)
                await Hydra.main.menu()