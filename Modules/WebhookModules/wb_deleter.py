import aiohttp


async def hdeleter(self):
    """Delete the webhook."""
    self.clear()
    self.send_logo()
    
    self.cmessage(" | Webhook URL >>: ",True)
    webhook = input()
    if await self.hcheck(webhook):
            self.cmessage("\n | Invalid Webhook URL. Try again!")
            input()
            await self.menu()
        
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(url=webhook) as response:
                    match response.status:
                         case 204:
                            self.cmessage(f"\n | [Success] >>> Deleted '{webhook}'")
                         case _:
                            self.cmessage(f"\n | [Failed] >>> {response.status}")
            except Exception as e:
                self.cmessage(f" [Error] Failed to delete webhook: {e}")
    except Exception as exp:
        print(exp)
        input()
        await self.menu()
            
    input()
    await self.menu()   