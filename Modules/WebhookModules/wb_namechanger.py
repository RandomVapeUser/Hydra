from colorama import Fore
import aiohttp
import asyncio

async def hnamechanger(self):
        """Change the webhook name"""
        self.clear()
        self.send_logo()

        self.cmessage(" | Webhook URL >>: ",True)
        self.webhook = input()

        if await self.hcheck():
            self.cmessage("\n | Invalid Webhook URL. Try again!")
            input()
            await self.menu()
            
        self.cmessage(" | Webhook New Name >>: ",True)
        hook_name = input()
        print()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url=self.webhook, json={"name": hook_name}) as response:
                    if response.status == 200:
                        print(Fore.GREEN + " [SUCCESS] ",end="")
                        self.cmessage(f" >>> Changed webhook name to '{hook_name}'")
                        input()
                        await self.menu()
                    else:
                        self.cmessage(f" [ERROR] Failed to change name. Status code: {response.status}")
                        asyncio.sleep(5)
            except Exception as e:
                self.cmessage(f" [Error] Exception during name change: {str(e)}")
                input()
                await self.menu()