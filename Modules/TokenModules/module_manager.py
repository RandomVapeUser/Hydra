from colorama import Fore
from typing import Literal
import requests
import aiohttp
import asyncio
import random
import uuid
import json
import sys
import os

cwd = os.getcwd() #Get Current Directory
parent_dtr = os.path.abspath(os.path.join(cwd, os.pardir)) #Current directory + file path
sys.path.append(parent_dtr) #Basicly allows me to import the other modules

from Modules import TextAssets as ta #Text Assets
from Modules import ScraperUtils as su #Scraping users utils
from Hydra import Hydra #Main class

class TokenModules(ta.AsciiAssets):
    """Modules Involving user tokens"""
    def __init__(self) -> None:
        self.cookies = self.getcookies()
        self.proxylist = []
        self.proxytype = None
        self.tokens = []
        
    def gettokens(self) -> None:    
        global token_amount
        self.tokens = []
        token_amount = 0
        with open("tokens.txt", "r") as tokens:
            for line in tokens:
                token = line.strip("\n")
                token_amount += 1
                self.tokens.append(token)

    async def joiner_menu(self) -> None:
        os.system("cls")
        self.gettokens()
        self.send_logo()
        self.cmessage("\n | Server Invite >>: ", True)
        self.invite = input()
        self.cmessage(" | Join Delay >>: ", True)
        self.delay = input()
        print("")

        async def joiner(self, token, invite):
            print("Test")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"https://discord.com/api/v9/invites/{str(invite).strip().split('/')[-1]}",
                        headers=self.headers(invite,"POST",token),
                        json={"session_id": uuid.uuid4().hex}
                    ) as response:
                        match response.status:  
                            case 200:
                                print(Fore.GREEN + "| [Joined] ", end="")
                                self.cmessage(f" >>: {token[:30]}***************************")
                            case 400:
                                print(Fore.YELLOW + "| [Captcha] ", end="")
                                self.cmessage(f" >>: {token[:30]}***************************")
                            case 429:
                                print(Fore.BLUE + "| [CloudFlare] ", end="")
                                self.cmessage(f" >>: {token[:30]}***************************")
                            case _:
                                print(Fore.RED + "| [Failed] ", end="")
                                self.cmessage(f" >>: {token[:30]}***************************")
            except Exception as e:
                self.cmessage(f"\n| Failed to initiate Token joiner: {e}")
                input()
                await Hydra.main.menu()

        tasks = []
        for token in self.tokens:
            task = asyncio.create_task(joiner(self,token,self.invite))
            tasks.append(task)
        await asyncio.gather(*tasks)
        
        input()
        await Hydra.main.menu()

    async def scraper(self):
        os.system("cls")
        self.send_logo()
        self.cmessage("\n| User token (Must be in server) >>: ",True)
        self.token = input()
        self.cmessage("| Server ID >>: ",True)
        self.guild_id = input()
        self.cmessage("| Any channel ID >>: ",True)
        self.channel_id = input()

        scrapeobj = su.DiscordSocket(self.token,self.guild_id,self.channel_id)
        scrapeobj.member_scrape(self.guild_id,self.channel_id)
        self.log(f"{Hydra.dnow} | User Scraper ; Server ID >>> {self.guild_id}")
        exit = input()
        await Hydra.main.menu()
    
    async def token_checker(self):
        global token_amount
        os.system("cls")
        self.send_logo()
        self.gettokens()

        Valid_list = []
        Locked_list = []
        Invalid_list = []

        async def checker(self,token):
            async with aiohttp.ClientSession() as session:
                async with session.get("https://discord.com/api/v9/users/@me/library", headers={"authorization": token}) as response:
                    final_token = token[:-20] + "***************"
                    match response.status:
                        case 200:
                            self.cmessage("| ",True)
                            print(Fore.GREEN + "[Valid Token] ", end="")
                            self.cmessage(f">>> {final_token}")
                            Valid_list.append(token)
                        case 403:
                            self.cmessage("| ",True)
                            print(Fore.YELLOW + "[Locked Token] ", end="")
                            self.cmessage(f">>> {final_token}")
                            Locked_list.append(token)
                        case _:
                            self.cmessage("| ",True)
                            print(Fore.RED + "[Invalid Token] ", end="")
                            self.cmessage(f">>> {final_token}")
                            Invalid_list.append(token)

        tasks = []
        for token in self.tokens:
            task = asyncio.create_task(checker(self,token))
            tasks.append(task)
        await asyncio.gather(*tasks)

        self.cmessage(f"\n| {len(Valid_list)} ",True)
        print(Fore.GREEN + "Valid tokens.")
        self.cmessage(f"| {len(Invalid_list)} ",True)
        print(Fore.RED + "Invalid tokens.")
        self.cmessage(f"| {len(Locked_list)} ",True)
        print(Fore.YELLOW + "Locked tokens.")

        self.cmessage("\n| Remove Invalid Tokens? (Y/N)\n| >>: ",True)
        choice = input().upper()
        if choice == "Y":
            existing_tokens = set()
            with open("tokens.txt", "r+") as f:
                existing_tokens.update(line.strip() for line in f if line.strip())
            updated_tokens = existing_tokens - set(Invalid_list) - set(Locked_list)
            token_list = list(updated_tokens)
            with open("tokens.txt", "w+") as f:
                f.write("\n".join(token_list) + "\n")
            token_amount -= len(Invalid_list) + len(Locked_list)
            self.cmessage(f"\n| Removed {len(Invalid_list)} Invalid Tokens, {len(Locked_list)} Locked Tokens!")
            
        exit = input()
        await Hydra.main.menu()

    async def channel_spammer(self):
        os.system("cls")
        self.gettokens()

        if not self.tokens:
            self.cmessage("\n| No tokens found, try again with tokens!")
            await asyncio.sleep(2)
            await Hydra.main.menu()

        self.send_logo()
        self.requests_made = 0
        self.proxy_index = 0
        self.cmessage(" | Server ID >>: ", True)
        server_id = input().strip()
        self.cmessage(" | Channel ID >>: ", True)
        channel_id = input().strip()
        self.cmessage(" | Message content >>: ", True)
        content = input().strip()
        self.cmessage(" | Enable Random Pings (Y/N) >>: ", True)
        enable_pings = input().strip().upper()
        self.cmessage(" | Enable Proxies (Y/N) >>: ", True)
        enable_proxies = input().strip().upper()
        self.cmessage(" | Amount of threads >>: ", True)
        self.threads = input().strip()
        print()

        await self.schecker(server_id)
        token_check_path = f"Data/Token_Checks/Server_ID_Check_{server_id}.txt"

        if not os.path.exists(token_check_path) or not os.path.getsize(token_check_path):
            self.cmessage("\n| No Tokens found in the server! Try again later.")
            await asyncio.sleep(2)
            await Hydra.main.menu()

        if enable_pings == "Y":
            with open(token_check_path, "r") as f:
                token = f.readline().strip()
                if token:
                    scrapeobj = su.DiscordSocket(token, server_id, channel_id)
                    scrapeobj.member_scrape(server_id, channel_id)
                    ids_path = f"scraped/{server_id}.txt"
                    if os.path.exists(ids_path):
                        ids = open(ids_path).read().splitlines()
                    else:
                        self.cmessage("\n| No scraped IDs found! Proceeding without pings.")
                        enable_pings = "N"
                else:
                    self.cmessage("\n| No valid token found for scraping! Proceeding without pings.")
                    enable_pings = "N"

        async def send_message(channel_id:str, message:str, token:str, proxy=None):
            async with aiohttp.ClientSession() as session:
                try:
                    while True:
                        if enable_proxies == "Y" and self.requests_made == 6:
                            self.requests_made = 0
                            self.proxy_index += 1
                            if len(self.proxylist) == 0:
                                self.cmessage("| No proxies available! Cannot continue.")
                                return
                            self.proxy_index = self.proxy_index % len(self.proxylist)
                            proxy = self.proxylist[self.proxy_index]
                            self.cmessage(f"| [Switching Proxy] >>> {proxy}")

                        if enable_proxies == "Y":
                            proxy = self.proxylist[self.proxy_index]
                        
                        async with session.post(
                            f"https://discord.com/api/v9/channels/{channel_id}/messages",
                            headers={"authorization":str(token)},
                            json={"content": message,"nonce": "1315434458647625728"},
                            proxy=proxy if enable_proxies == "Y" else None
                        ) as response:
                            match response.status:
                                case 200:
                                    print(Fore.GREEN + " | [Sent] ", end="")
                                    self.cmessage(f">>: {token[:30]}***************************")
                                case 429:
                                    print(Fore.YELLOW + " | [Ratelimit] ", end="")
                                    self.cmessage(f">>: {token[:25]}***************************")
                                case _:
                                    print(Fore.RED + " | [Failed] ", end="")
                                    self.cmessage(f">>: {token[:25]}*************************** | {response.status} {response.reason}")
                            self.requests_made += 1
                except IndexError as e:
                    self.cmessage(f"\n | IndexError: {str(e)}")
                    return
                except Exception as e:
                    self.cmessage(f"\n | Error sending message >>: {str(e)}")
                    input()

        if enable_proxies == "Y" and len(self.proxylist) == 0:
            self.cmessage("\n | No proxies available! Please enter some in proxies.txt!")
            input()
            await Hydra.main.menu()
        if enable_pings == "Y" and (not ids or len(ids) == 0):
            self.cmessage("| No valid member IDs found for pings!")
            enable_pings = "N" 

        tasks = []

        if enable_pings == "Y" and enable_proxies == "Y":
            self.load_proxies()
            if len(self.proxylist) == 0:
                self.cmessage("| No proxies available! Cannot continue.")
                return
            for token in self.tokens:
                ping_ids = random.sample(ids, 3)
                content_with_pings = f"{content} >> <@{ping_ids[0]}> | <@{ping_ids[1]}> | <@{ping_ids[2]}>"
                tasks.append(send_message(channel_id, content_with_pings, token))
            await asyncio.gather(*tasks)
        elif enable_pings == "Y" and enable_proxies == "N":
            for _ in range(int(self.threads)):
                ping_ids = random.sample(ids, 3)
                content_with_pings = f"{content} >> <@{ping_ids[0]}> | <@{ping_ids[1]}> | <@{ping_ids[2]}>"
                for token in self.tokens:
                    tasks.append(send_message(channel_id, content_with_pings, token))

            await asyncio.gather(*tasks)
        elif enable_pings == "N" and enable_proxies == "Y":
            self.load_proxies()
            if len(self.proxylist) == 0:
                self.cmessage("| No proxies available! Cannot continue.")
                return

            for token in self.tokens:
                tasks.append(send_message(channel_id, content, token))

            await asyncio.gather(*tasks)
        else:
            for _ in range(int(self.threads)):
                for token in self.tokens:
                    tasks.append(send_message(channel_id, content, token))

            await asyncio.gather(*tasks)



    async def formatter(self):
        os.system("cls")
        super().send_logo()
        self.cmessage(f"\n| [Path to File] >>: ",True)
        path = input().strip()

        if not os.path.isfile(path):
            self.cmessage("\n| [Error] >>> Invalid Path!")
            input()
            await Hydra.main.menu()

        tokens = []
        fpath = os.path.join(os.path.dirname(path), "/Data/Token_Checks/Formated_Tokens.txt")

        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    tokens.append(parts[2])

        with open(fpath, 'w') as f:
            for token in tokens:
                f.write(token + '\n')

        self.cmessage("\n| Saved tokens to /Data/Token_Checks/Formated_Tokens.txt")
        self.cmessage("| Add formated tokens? (Y/N) \n| >>: ",True)
        choice = input()

        if choice.upper().startswith("Y"):
            with open("tokens.txt","a+") as token_file:
                for i in tokens:
                    final_token = i.strip()
                    token_file.write(f"{final_token}\n")
        
        self.cmessage("| Successfully Added tokens!",True)
        input()
        await Hydra.main.menu()

    async def schecker(self,server_id):
        self.gettokens()
        async with aiohttp.ClientSession() as session:
            for token in self.tokens:
                with open(f"Data/Token_Checks/Server_ID_Check_{server_id}.txt","w+") as f:
                    async with session.get(f"https://discord.com/api/v9/guilds/{int(server_id)}", headers={"authorization": token}) as response:
                        match response.status:
                            case 204:
                                f.write(token)
                            case 200:
                                f.write(token)

    async def server_checker(self):
        os.system("cls")
        self.send_logo()
        self.cmessage("[Server ID] >>: ",True)
        self.gettokens()

        try:
            server_id = input()
        except ValueError:
            self.cmessage("Invalid Server ID.")
            exit = input()
            await Hydra.main.menu()

        async with aiohttp.ClientSession() as session:
            for token in self.tokens:
                headers = {    
                    "authorization": token,
                    "Content-Type": "application/json"
                }
                with open(f"token_checks/Server_ID_Check_{server_id}.txt","a+") as f:
                    async with session.get(f"https://discord.com/api/v9/guilds/{int(server_id)}", headers=headers) as response:
                        match response.status:
                            case 200:
                                print(Fore.GREEN + "[In Server] ", end="")
                                self.cmessage(f">>: {token[:30]}***************************")
                                f.write(token)
                            case _:
                                print(Fore.RED + "[Not in Server] ", end="")
                                self.cmessage(f">>: {token[:25]}***************************")
            
        exit = input()
        await Hydra.main.menu()

    async def bio_changer(self):
        os.system("cls")
        self.send_logo()
        self.gettokens()
        if self.tokens == []:
            self.cmessage("\nNo tokens found! Try again when you have added tokens!")
            await asyncio.sleep(2)
            await Hydra.main.menu()

        self.cmessage("""                  
        | Statuses
        | [1] @~> Online
        | [2] @~> Idle
        | [3] @~> Busy
        | [4] @~> Offline
        
        | [Status] >>:  """,True)
        status = input("")
        print(" ")
        async def change_status(token,status):
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"https://discord.com/api/v9/users/@me/settings-proto/1", headers=self.headers(), json={"settings" : status}) as response:
                    match response.status:
                        case 200:
                            print(Fore.GREEN + "        [Successfully changed status]", end="")
                            self.cmessage(f" >>> {token[:25]}*********************")
                        case _:
                            print(Fore.RED + "[Failed to change status]", end="")
                            self.cmessage(f"Failed Changing bio, code {response.status}")
        statuses = {
            "1" : "WgoKCAoGb25saW5l",
            "2" : "WggKBgoEaWRsZQ==",
            "3" : "WgcKBQoDZG5k",
            "4" : "Wg0KCwoJaW52aXNpYmxl"
        }

        if status in statuses:
            tasks = []
            for token in self.tokens:
                tasks.append(asyncio.create_task(change_status(token,statuses[status])))
            await asyncio.gather(*tasks)
        else:
            self.cmessage("Option not found! Returning to the menu...")
            await asyncio.sleep(3)
            await Hydra.main.menu()

        await asyncio.sleep(4)
        await Hydra.main.menu()

    async def accept_rules(self):
        os.system("cls")
        self.gettokens()
        self.send_logo()
        self.cmessage("| [Server ID] >>: ",True)
        server_id = input()
        print()

        if self.tokens != []:
            async def change_status(token,server_id): 
                headers = {
                    "authorization": token
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put(f"https://discord.com/api/v9/guilds/{server_id}/requests/@me", headers=headers) as response:
                        match response.status:
                            case 200:
                                print(Fore.GREEN + "[Accepted Rules]", end="")
                                self.cmessage(f" >>> {token[:25]}*********************")
                            case 410:
                                print(Fore.RED + "[Rules embed not found]", end="")
                                self.cmessage(f" >>> {token[:25]}*********************")
                            case 403:
                                print(Fore.RED + "[Server not Found]", end="")
                                self.cmessage(f" >>> {token[:25]}*********************")
                            case _:
                                print(Fore.RED + "[Failed to accept rules]", end="")
                                self.cmessage(f" >>> {token[:25]}*********************")

            tasks = []
            for token in self.tokens:
                task = asyncio.create_task(change_status(token,server_id))
                tasks.append(task)
            await asyncio.gather(*tasks)

            input()
            await Hydra.main.menu()
        else:
            self.cmessage("\n| No Tokens Found! Try again later.")
            input()
            await Hydra.main.menu()
            
            
    async def name_changer(self):
        os.system("cls")
        self.send_logo()
        self.gettokens()
        if self.tokens == []:
            self.cmessage("\nNo tokens found! Try again when you have added tokens!")
            await asyncio.sleep(2)
            await Hydra.main.menu()
        self.cmessage("| New Username >>: ",True)
        new_name = input()
        print()
        async def change_name(token,new_name):
            headers = {
                "authorization": token,
                "Content-Type": "application/json"
            }
            async with aiohttp.ClientSession() as session:
                async with session.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"username": new_name}) as response:
                    match response.status:
                        case 200:
                            print(Fore.GREEN + "[Changed Name]", end="")
                            self.cmessage(f" >>> {token[:25]}*********************")
                        case 429:
                            print(Fore.YELLOW + "[Ratelimited]", end="")
                            self.cmessage(f" >>> {token[:25]}*********************")
                        case _:
                            print(Fore.RED + "[Failed to change name]", end="")
                            self.cmessage(f" >>> {token[:25]}*********************")
        tasks = []
        for token in self.tokens:
            tasks.append(asyncio.create_task(change_name(token,new_name)))
        await asyncio.gather(*tasks)
        await asyncio.sleep(4)
        await Hydra.main.menu()
