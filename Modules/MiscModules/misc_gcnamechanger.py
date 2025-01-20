from names_generator import generate_name
from colorama import Fore
import aiohttp
import asyncio

async def gcnamechanger(self):
        self.clear()
        self.send_logo()
        
        tchanged = 0
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
        super().log(f"{self.dnow} | Group Name Changer Spammer >> Channel ID : {self.channel_id}")
        print()

        self.headers = {
            "Origin" : "https://canary.discord.com",
            "authorization" : self.token,
            "Content-Type" : "application/json"
        }

        async def gcsp(self,channel_id):
            try:
                random_name = generate_name()
                async with aiohttp.ClientSession() as session:
                    async with session.patch(url=f"https://discord.com/api/v9/channels/{channel_id}",headers=self.headers, json={"name": random_name}) as response:
                        match response.status:
                            case 200:
                                print(Fore.GREEN + "[Changed Name] ",end="")
                                self.cmessage(f">>> '{random_name}' | {self.dnow}")
                            case 429:
                                print(Fore.YELLOW + "[Ratelimited] ",end="")
                                self.cmessage(f">>> '{random_name}' | {self.dnow}")
                            case _:
                                self.cmessage(f"[Failed] Failed to Spam URL: {response.status}")
            except Exception as e:
                self.cmessage(f"[ERROR] Failed to Spam URL: {str(e)}")
                input()
                self.menu()
    
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
            except Exception as e:
                print(f"\n{e}")
                input()
                await self.menu()