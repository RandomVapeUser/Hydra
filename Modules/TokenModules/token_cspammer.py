from colorama import Fore
import aiohttp
import asyncio
import random
import os 

async def channel_spammer(self):
    self.send_logo()
    print("e")
    self.get_tokens()
    await self.ctokens()
    self.load_proxies()
    
    self.requests_made = 0
    self.proxy_index = 0

    while True:
        try:
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
            break
        except Exception:
            self.cmessage(f"\n| Error >>: {Exception}\n| Invalid Values?, please check the input entered before making a mistake.")
    
    print()

    await self.schecker(server_id)
    token_check_path = f"Data/Token_Checks/SIDC_{server_id}.txt"

    self.headers = await self.gheaders(channel_id, "POST", self.tokens[0])

    #Main spamming function 
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
                        headers=self.headers,
                        json= {
                            "content": message,
                            "cookie": self.getcookies},
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

    #Returns content with random pings
    def content_with_pings(content:str, ping_ids: list):
        return f"{content} >> <@{ping_ids[0]}> | <@{ping_ids[1]}> | <@{ping_ids[2]}>"
    
    #Scrapes IDs
    if enable_pings == "Y":
        with open(token_check_path, "r") as f:
            token = f.readline().strip()
            if token:
                scrapeobj = self.su.DiscordSocket(token, server_id, channel_id)
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

    #Checks if proxies.txt has proxies or not
    if enable_proxies == "Y" and len(self.proxylist) == 0:
        self.cmessage("\n | No proxies available! Please enter some in proxies.txt!")
        input()
        await self.Hydra.main.menu()
    if enable_pings == "Y" and (not ids or len(ids) == 0):
        self.cmessage("| No valid member IDs found for pings!")
        enable_pings = "N" 

    tasks = []
    # Random Pings && Proxies
    if enable_pings == "Y" and enable_proxies == "Y":
        self.load_proxies()
        if len(self.proxylist) == 0:
            self.cmessage("| No proxies available! Cannot continue.")
            return
        for token in self.tokens:
            ping_ids = random.sample(ids, 3)
            tasks.append(send_message(channel_id, content_with_pings(content, ping_ids), token))
        await asyncio.gather(*tasks)

    # Random Pings No Proxies
    elif enable_pings == "Y" and enable_proxies == "N":
        for _ in range(int(self.threads)):
            ping_ids = random.sample(ids, 3)
            for token in self.tokens:
                tasks.append(send_message(channel_id, content_with_pings(content, ping_ids), token))
        await asyncio.gather(*tasks)

    # No Pings && Proxies
    elif enable_pings == "N" and enable_proxies == "Y":
        self.load_proxies()
        if len(self.proxylist) == 0:
            self.cmessage("| No proxies available! Cannot continue.")
            return
        for token in self.tokens:
            tasks.append(send_message(channel_id, content, token))
        await asyncio.gather(*tasks)
    else:
        # No Pings No Proxies
        for _ in range(int(self.threads)):
            for token in self.tokens:
                tasks.append(send_message(channel_id, content, token))
        await asyncio.gather(*tasks)