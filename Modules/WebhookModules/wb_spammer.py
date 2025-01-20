from colorama import Fore
import aiohttp
import asyncio

async def hspammer_menu(self):
    """Spam the webhook with messages."""
    self.clear()
    self.send_logo()

    self.cmessage("| Webhook URL >>: ", True)
    self.webhook = input()
    self.hcheck()

    self.cmessage("| Message >>: ", True)
    self.message = input()

    self.cmessage("| Threads (Not recommended 5+ threads) >>: ", True)
    try:
        self.threads = int(input())
        raise Exception if self.threads <= 0 else None
    except Exception:
        self.cmessage("Threads must be an integer higher than 0!")
        input()
        await self.menu()

    self.cmessage("| Delay >>: ", True)
    try:
        self.delay = float(input())
        raise Exception if self.threads <= 0 else None
    except Exception:
        self.cmessage("Delay must be a float higher than 0!")
        input()
        await self.menu()


    print()
    async def hspammer(message):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.post(url=self.webhook, json={"content": message}) as response:
                        match response.status:
                            case 204:
                                print(Fore.GREEN + "| [SENT] ", end="")
                                self.cmessage(f">>> '{message}' | {self.dnow}")
                            case 429:
                                print(Fore.YELLOW + "| [Ratelimit] ", end="")
                                self.cmessage(f">>> '{message}' | {self.dnow}")
                            case _:
                                self.cmessage(f"[Failed] Status {response.status} - Failed to Spam URL")
                                input()
                                break
                except Exception as e:
                    self.cmessage(f"[ERROR] Network error: {str(e)}")
                    input()
                    break

    tasks = []
    for _ in range(self.threads):
        await asyncio.create_task(hspammer(self.message))
    await asyncio.gather(*tasks)