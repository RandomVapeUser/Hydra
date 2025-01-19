from colorama import Fore
import aiohttp

async def invite_info(self):
        self.clear()
        self.send_logo()

        self.cmessage("\n| Server invite >>: ",True)
        invite = input()
        finvite = invite.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/invites/{finvite}") as response:
                if response.status == 200:
                    data = await response.json()
                    security_level = data['guild']['verification_level']
                    guild_id = data['guild']['id']
                    inviter = data.get('inviter', {})
                    self.cmessage(f"\n| Server Data >>> {data['guild']['name']} ({guild_id})")
                    self.cmessage(f"| Server Description >>> {data['guild']['description']}.\n")
                    match security_level:
                        case 0:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (No Protection!)")
                        case 1:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required!)")
                        case 2:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 5 minutes!)")
                        case 3:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 10 minutes!)")
                        case 4:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Verified Email Required! + Been in the server for 5 minutes! + Verified Phone Number!)")                    
                        case _:
                            self.cmessage(f"| Server Security Level 👮‍♂️ ~~> Level {security_level} (Unknown)")
                    if inviter:
                        self.cmessage(f"| Inviter ~~> {data['inviter']['username']} ({data['inviter']['id']})")
                    else:
                         self.cmessage(f"| Inviter ~~> Vanity Invite ({finvite})")
                    if "AUTO_MODERATION" in data['guild']['features']:
                        self.cmessage("| AutoMod 🤖 ~~> ",True)
                        print(Fore.GREEN + "True")
                    else:
                        self.cmessage("| AutoMod 🤖 ~~> ",True)
                        print(Fore.RED + "False")
                    input()
                    await self.menu() 
                else:
                    self.cmessage("\nInvalid Discord link, the correct format is Ex.'https://discord.gg/g4eaH7EQJq'.")
                    exit = input()
                    await self.menu() 