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
    "2" : "RED",
    "3" : "BLUE",
    "4" : "ORANGE"
}

class Main(Assets.AsciiAssets):
    """
    Main class to handle menu
    """
    
    def __init__(self):
        """
        Initializer for Main class
        """
        self.tokens = []
        self.tokenamount = 0
        self.dnow = str(datetime.datetime.now().strftime("%H:%M:%S"))

    def clear(self) -> None:
        """
        Clear the console
        """
        os.system("cls" if os.name == "nt" else "clear")

    def get_tokens(self) -> None:
        """
        Updates Token List
        """
        with open("Data/tokens.txt", "r+") as tokens:
            for token in tokens:
                self.tokens.append(token.strip())
            self.tokenamount = len(self.tokens)

    async def ctokens(self) -> None:
        """
        Check if tokens exist
        """
        with open("Data/tokens.txt", "r+") as tokens:
            if tokens.read().strip() == "":
                self.cmessage("\n| No tokens found, try again with tokens!"); input()
                await self.menu()

    async def hcheck(self, webhook) -> None:
        """
        Check webhook status code (validate webhook)
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(webhook) as response:
                    match response.status:
                        case 200:
                            pass
                        case _:
                            self.cmessage("\n | Invalid Webhook URL. Try again!"); input()
                            await self.menu()
            except Exception:
                self.cmessage("\n | Invalid Webhook URL. Try again!"); input()
                await self.menu()  

    async def choice_manager(self, choice: str) -> None:
        """
        Manager for choices
        """
        choices = {
            "1" : [["1", "2", "3"], "webhooks", self.main_text[1]],
            "2" : [["1", "2", "3", "4", "5", "6", "7", "8", "9"], "tokens", self.main_text[0]],
            "3" : [["1", "2"], "misc", self.main_text[2]],
            "4" : self.settings,
            "5" : self.credits
        }
 
        if choice in ["4", "5"]:
            await choices[choice]()

        while True:

            self.clear()
            self.send_logo()
            self.cmessage(choices[choice][2], True)
            module_choice = input().strip()

            if module_choice in choices[choice][0]:
                await manager.select_module(self, choices[choice][1], module_choice) 
            elif module_choice == "<<":
                await self.menu()
                break
            else:
                continue
            
    async def settings(self) -> None:
        """
        Hydra Settings Menu
        """
        global themes
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
                    new_config = {
                        "theme": themes[theme]
                        }
                    with open("config.json", "w") as config:
                        json.dump(new_config, config, indent=4)
                    
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
        """
        Credits menu
        """
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
        """
        Main menu for users
        """
        while True:
            self.clear()
            self.get_tokens()
            os.system(f"        title Hydra Multitool ^| Loaded {self.tokenamount} tokens ^| Version 0.6.2 Recoded by salomao31_termedv2")
            self.send_logo()
            self.cmessage(f"\n        [Token Amount] -> Loaded {self.tokenamount} tokens!")
            self.cmessage(self.main_text[6],True)

            choice = input().strip()
            if choice in ["1", "2", "3", "4", "5"]:
                await self.choice_manager(choice)
            else:
                continue
