from colorama import Fore
import aiohttp
import asyncio

async def accept_rules(self) -> None:
        self.clear()
        self.gettokens()
        self.send_logo()
        self.notokens()

        self.cmessage("| [Server ID] >>: ",True)
        server_id = input()
        print()

        async def change_status(token,server_id) -> None: 
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
        await self.Hydra.main.menu()