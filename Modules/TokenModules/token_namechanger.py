from colorama import Fore
import aiohttp
import asyncio
async def name_changer(self) -> None:
    self.clear()
    self.send_logo()
    self.gettokens()
    self.notokens()

    self.cmessage("| New Username >>: ",True)
    new_name = input()
    print()

    #Spamming function
    async def change_name(token,new_name) -> None:
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

    #Asyncio task spammer
    tasks = []
    for token in self.tokens:
        tasks.append(asyncio.create_task(change_name(token,new_name)))
    await asyncio.gather(*tasks)
    
    #Exit
    input()
    await self.Hydra.main.menu()