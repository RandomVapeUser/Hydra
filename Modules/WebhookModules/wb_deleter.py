import aiohttp

async def hdeleter(self):
        """Delete the webhook."""
        self.clear()
        self.send_logo()

        self.cmessage(" | Webhook URL >>: ",True)
        self.webhook = input()
        await self.hcheck()
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(url=self.webhook) as response:
                    match response.status:
                         case 204:
                            self.cmessage(f"\n | [Success] >>> Deleted '{self.webhook}'")
                         case _:
                            self.cmessage(f"\n | [Failed] >>> {response.status}")
            except Exception as e:
                self.cmessage(f" [Error] Failed to delete webhook: {str(e)}")
        input()
        await self.menu()   