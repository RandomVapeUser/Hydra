from colorama import Fore
import aiohttp
import asyncio

async def token_checker(self) -> None:
    self.send_logo()
    self.gettokens()

    Valid_list = []
    Locked_list = []
    Invalid_list = []

    async def checker(self,token) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v9/users/@me/library", headers={"authorization": token}) as response:
                final_token = token[:-20] + "***************"
                match response.status:
                    case 200:
                        self.cmessage("| ",True)
                        print(Fore.GREEN + "[Valid Token] ", end="")
                        self.cmessage(f"-> {final_token}")
                        Valid_list.append(token)
                    case 403:
                        self.cmessage("| ",True)
                        print(Fore.YELLOW + "[Locked Token] ", end="")
                        self.cmessage(f"-> {final_token}")
                        Locked_list.append(token)
                    case _:
                        self.cmessage("| ",True)
                        print(Fore.RED + "[Invalid Token] ", end="")
                        self.cmessage(f"-> {final_token}")
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

        self.tokenamount -= len(Invalid_list) + len(Locked_list)
        self.cmessage(f"\n| Removed {len(Invalid_list)} Invalid Tokens, {len(Locked_list)} Locked Tokens!")
        
    input()
    await self.Hydra.main.menu()