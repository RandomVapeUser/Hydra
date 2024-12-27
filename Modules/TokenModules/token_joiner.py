from colorama import Fore
import aiohttp
import asyncio
import uuid
import os

async def joiner_menu(self) -> None:
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
                await self.Hydra.main.menu()

        tasks = []
        for token in self.tokens:
            task = asyncio.create_task(joiner(self,token,self.invite))
            tasks.append(task)
        await asyncio.gather(*tasks)
        
        input()
        await self.Hydra.main.menu()