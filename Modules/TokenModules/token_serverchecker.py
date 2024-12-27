from colorama import Fore
import aiohttp

async def server_checker(self) -> None:
        self.clear()
        self.send_logo()
        self.cmessage("[Server ID] >>: ",True)
        self.gettokens()

        try:
            server_id = input().strip()
        except ValueError:
            self.cmessage("Invalid Server ID.")
            input()
            await self.Hydra.main.menu()

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
            
        input()
        await self.Hydra.main.menu()