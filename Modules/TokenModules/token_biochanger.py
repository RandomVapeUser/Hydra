from colorama import Fore
import asyncio
import aiohttp

async def bio_changer(self) -> None:
    self.clear()
    self.send_logo()
    self.gettokens()
    if self.tokens == []:
        self.cmessage("\n| No tokens found! Try again when you have added tokens!")
        input()
        await self.Hydra.main.menu()
    self.cmessage("""                  
    | Statuses
    | [1] -> Online
    | [2] -> Idle
    | [3] -> Busy
    | [4] -> Offline
    
    | [Status] >>:  """,True)
    status = input("")
    print(" ")
    async def change_status(token,status):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"https://discord.com/api/v9/users/@me/settings-proto/1", headers=self.headers(), json={"settings" : status}) as response:
                match response.status:
                    case 200:
                        print(Fore.GREEN + "\n| Successfully changed status")
                        self.cmessage(f" >>> {token[:25]}*********************")
                    case _:
                        print(Fore.RED + "\n| Failed to change status")
                        self.cmessage(f"\n| Failed Changing bio, code {response.status}")
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
        input()
        await self.Hydra.main.menu()
    input()
    await self.Hydra.main.menu()