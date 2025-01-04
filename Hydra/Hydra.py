from Hydra import Assets
import datetime
import aiohttp
import json
import sys
import os

parent_dirct = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dirct[:-6])
from Modules import ModuleManager as md

manager = md.ModuleManager()
dr = os.path.join(os.getcwd(), "Data/tokens.txt")
if not os.path.isfile(dr):
    open(dr, "w")

config = json.load(open("config.json", "r+"))
Assets.AsciiAssets.set_theme(config["theme"].upper())

themes = {
    "1" : "DEFAULT",
    "2" : "BLUE",
    "3" : "ORANGE",
    "4" : "RED"
}

class Main(Assets.AsciiAssets):
    """Main class to handle menu"""
    def __init__(self):
        self.tokens = []
        self.dnow = str(datetime.datetime.now().strftime("%H:%M:%S"))
    
    tokenamount = 0
    
    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def get_tokens(self) -> None:
        """Updates Token List"""
        with open("Data/tokens.txt", "r+") as tokens:
            for token in tokens:
                self.tokens.append(token.strip())
            self.tokenamount = len(self.tokens)

    async def ctokens(self) -> None:
        with open("Data/tokens.txt", "r+") as tokens:
            if tokens.read().strip() == "":
                self.cmessage("\n| No tokens found, try again with tokens!")
                input()
                await self.menu()

    async def hcheck(self) -> None:
        """Check webhook status code (validate webhook)."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.webhook) as response:
                    match response.status:
                        case 200:
                            pass
                        case _:
                            self.cmessage("\n| Invalid Webhook URL. Try again!")
                            input()
                            await self.menu()
            except Exception:
                self.cmessage("\n| Invalid Webhook URL. Try again!")
                input()
                self.menu()  
                
    async def choice_manager(self, choice: int) -> None:
        choices = {
            1 : [[1,2,3,4,5,6,7,8,9], "tokens",self.main_text[1]],
            2 : [[1,2,3,4],"webhooks",self.main_text[0]],
            3 : [[1,2,3],"misc",self.main_text[2]],
            4 : self.settings,
            5 : self.credits
        }
        if choice in [4,5]:
            await choices[choice]()

        self.clear()
        self.send_logo()
        self.cmessage(choices[choice][2],True)
        choice = input().strip()

        match choice:
            case "<<":
                await self.menu()
            case _ if int(choice) in [1,2,3]:
                await manager.select_module(choices[choice][1],choice)
            case _:
                self.cmessage("\n | Invalid Option try again.")
                input()
            
    async def settings(self) -> None:
        """Hydra Settings Menu"""
        self.clear()
        self.send_logo()
        self.cmessage(self.main_text[3], True)
        option = input().strip()
        match option:
            case "1":
                self.clear()
                self.send_logo()
                self.cmessage(self.main_text[4], True)
                theme = input().strip()

                if theme in themes.keys():
                    with open("config.json", "r+") as file:
                        config = json.load(file)
                    config["theme"] = themes[theme]

                    with open("config.json", "w") as file:
                        json.dump(config, file, indent=4)
                        
                    self.cmessage("\n        | Theme has been updated, restart Hydra to complete change.")
                    input()
                    await self.menu()
                else:
                    self.cmessage("\n        | Invalid theme choice.")
                    input()
                    await self.menu()
            case _:
                await self.menu()

    async def credits(self) -> None:
        while True:
            self.clear()
            self.send_logo()
            self.cmessage(self.main_text[5], True)
            op = input()
            if op != "<<":
                continue
            else:
                break
        await self.menu()

    async def menu(self) -> None:
        """Main menu for users"""
        while True:
            self.clear()
            self.get_tokens()
            os.system(f"        title Hydra Multitool ^| Loaded {self.tokenamount} tokens ^| Version 0.6 Recoded by Sal")
            self.send_logo()
            self.cmessage(f"        [Token Amount] ~> Loaded {self.tokenamount} tokens!")
            self.cmessage(self.main_text[6],True)

            choice = input().strip()
            try:
                if int(choice) in [1,2,3,4,5,6,7,8,8]:
                    await self.choice_manager(int(choice))
                elif choice == "XX":
                    sys.exit()
                else:
                    continue
            except Exception:
                continue
