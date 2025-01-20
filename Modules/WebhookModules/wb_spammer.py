from colorama import Fore
import aiohttp
import asyncio

hd_self = None
async def hspammer_menu(self):
    """Spam the webhook with messages."""
    global hd_self
    self.clear()
    self.send_logo()
    hd_self = self

    self.cmessage(" | Webhook URL >>: ", True)
    webhook = input()
    await self.hcheck(webhook)

    self.cmessage(" | Message >>: ", True)
    message = input()

    self.cmessage(" | Threads (Not recommended 5+ threads) >>: ", True)
    threads = input().strip()
    if int(threads) <= 0:
        self.cmessage(" Threads must be higher than 0!")
        input()
        await self.menu()

    self.cmessage("| Delay >>: ", True)
    delay = input().strip()
    if int(self.delay) < 0:
        self.cmessage(" Delay must be positive! (0 included)")
        input()
        await self.menu()
        
    print()
    async def hspammer(message):
        async with aiohttp.ClientSession() as session:
            while True:
                await asyncio.sleep(float(delay))
                try:
                    async with session.post(url=webhook, json={"content": message}) as response:
                        match response.status:
                            case 204:
                                print(Fore.GREEN + " | [Sent] ", end="")
                                hd_self.cmessage(f">>> '{message}' | {hd_self.dnow}")
                            case 429:
                                print(Fore.YELLOW + " | [Ratelimit] ", end="")
                                hd_self.cmessage(f">>> '{message}' | {hd_self.dnow}")
                            case _:
                                hd_self.cmessage(f"[Failed] Status {response.status} - Failed to Spam URL.")
                                input()
                                break
                except Exception as e:
                    hd_self.cmessage(f"[ERROR] Network error: {str(e)}")
                    input()
                    break

    tasks = []
    for _ in range(threads):
        await asyncio.create_task(hspammer(message))
    await asyncio.gather(*tasks)