from colorama import Fore
import aiohttp

async def hnamechanger(self):
    try:
        """Change the webhook name"""
        print("Test")
        self.clear()
        self.send_logo()

        self.cmessage(" | Webhook URL >>: ",True)
        webhook = input()
        if await self.hcheck(webhook):
            self.cmessage("\n | Invalid Webhook URL. Try again!")
            input()
            await self.menu()

        self.cmessage(" | Webhook New Name >>: ",True)
        hook_name = input().strip()

        print()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url=webhook, json={"name": hook_name}) as response:
                    if response.status == 200:
                        print(Fore.GREEN + " | [SUCCESS] ",end="")
                        self.cmessage(f" >>> Changed webhook name to '{hook_name}'")
                        input()
                        await self.menu()
                    else:
                        self.cmessage(f" [ERROR] Failed to change name. Status code: {response.status}")
                        input()
                        await self.menu()
            except Exception as e:
                self.cmessage(f" [Error] Exception during name change: {e}")
                input()
                await self.menu()
    except Exception:
        print(Exception)
        input()