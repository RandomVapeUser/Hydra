from colorama import Fore
from typing import *
import aiohttp
import asyncio
import sys
import os

cwd = os.getcwd()
parent_dtr = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(parent_dtr)
from Modules import TextAssets as ta
from Hydra import Hydra

class WebhookModules(ta.AsciiAssets):
    """All Webhook related functions for the Multitool."""
    def __init__(self, ):
        self.webhook =      

    async def hnamechanger(self):
        """Change the webhook name."""
        os.system("cls")
        super().send_logo()
        self.cmessage("| Webhook URL >>: ",True)
        self.webhook = input()

        if await self.hcheck() != 200:
            self.cmessage("\n| Invalid Webhook URL. Try again!")
            exit = input()
            await Hydra.main.menu()
            
        self.cmessage("| Webhook New Name >>: ",True)
        hook_name = input()
        print()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(url=self.webhook, json={"name": hook_name}) as response:
                    if response.status == 200:
                        print(Fore.GREEN + "[SUCCESS] ",end="")
                        self.cmessage(f" >>> Changed webhook name to '{hook_name}'")
                        super().log(f"{Hydra.dnow} | Webhook Name Changer >>> {self.webhook}")
                        exit = input()
                        await Hydra.main.menu()
                    else:
                        self.cmessage(f"[ERROR] Failed to change name. Status code: {response.status}")
                        asyncio.sleep(5)
            except Exception as e:
                self.cmessage(f"[Error] Exception during name change: {str(e)}")
                asyncio.sleep(5)

    async def hinfo(self):
        """Retrieve webhook information."""
        os.system("cls")
        super().send_logo()
        self.cmessage("| Webhook URL >>: ",True)
        self.webhook = input()

        if await self.hcheck() != 200:
            self.cmessage("\nInvalid Webhook URL. Try again!")
            await asyncio.sleep(2)
            await Hydra.main.menu()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=self.webhook) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.cmessage(f"\n[Server ID] >> {data['guild_id']}")
                        self.cmessage(f"[Channel ID] >> {data['channel_id']}")
                        self.cmessage(f"[Webhook Name] >> {data['name']}")
                        self.cmessage(f"[Webhook Token] >> {data['token']}")
                        super().log(f"{Hydra.dnow} | Webhook Info >>> {self.webhook}")
                    else:
                        self.cmessage(f"\n| Failed to get webhook info, try again later!")
            except Exception as e:
                self.cmessage(f"\n| Failed to get webhook info: {str(e)}")

        exit = input()
        await Hydra.main.menu()
