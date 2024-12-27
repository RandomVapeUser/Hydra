from AuthAPI.authAPI import api
from Hydra import Hydra as hd
from Hydra import Assets
from time import sleep
import asyncio
import hashlib
import json
import time
import sys
import os

os.system("title Hydra Multitool")
themes = ["DEFAULT", "RED", "BLUE", "ORANGE"]
with open("config.json", "r+") as settings:
    data = json.load(settings)
    theme_setting = str(data.get("themes", "DEFAULT")).upper()
    if theme_setting in themes:
        Assets.AsciiAssets.set_theme(theme_setting)
    else:
        Assets.AsciiAssets.set_theme("DEFAULT")

class MainAuth(Assets.AsciiAssets):

    def getchecksum():
        md5_hash = hashlib.md5()
        file = open(''.join(sys.argv), "rb")
        md5_hash.update(file.read())
        digest = md5_hash.hexdigest()
        return digest


    keyauthapp = api(
        name = "Hydra", 
        ownerid = "ll4Ig0GWmE", 
        version = "1.0", 
        hash_to_check = getchecksum()
    )

    def start_hydra(self):
        if __name__ == "__main__":
            asyncio.run(hd.main.menu())

    def answer(self):
        while True:

            os.system("cls")
            self.send_logo()
            try:
                self.cmessage("""
    | [1] - Login
    | [2] - Register
    |
    | >>:  """,True)
                ans = input()
                if ans == "1":
                    os.system("cls")
                    self.send_logo()
                    self.cmessage("  | Username: ",True)
                    user = input()
                    self.cmessage("  | Password: ",True)
                    password = input()
                    x = self.keyauthapp.login(user, password)
                    if x == "invalid":
                        continue
                    else:
                        time.sleep(1.3)
                        self.start_hydra()
                        break
                elif ans == "2":
                    os.system("cls")
                    self.send_logo()
                    self.cmessage("  | Username: ",True)
                    user = input()
                    self.cmessage("  | Password: ",True)
                    password = input()
                    self.cmessage("  | License Key: ",True)
                    license = input()
                    x = self.keyauthapp.register(user, password, license)
                    if x == "invalid":
                        continue
                else:
                    self.cmessage("\n  | Invalid option.")
                    sleep(1)
                    os.system("cls")
                    self.answer()
            except KeyboardInterrupt:
                os._exit(1)

if __name__ == "__main__":
    main = MainAuth()
    main.answer()
else:
    os.system("cls")
    Assets.cmessage("\n| File cannot be executed in sandbox mode, please try again in a normal environment.")
    sleep(3)
    sys.exit()

