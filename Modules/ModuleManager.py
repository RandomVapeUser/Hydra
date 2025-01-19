import requests
import aiohttp
import json
import sys
import os

parent_dirct = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dirct)
from TokenModules import (
    token_cspammer,
    token_joiner,
    token_checker,
    token_ruleaccept,
    token_formatter,
    token_serverchecker,
    token_scraper,
    token_biochanger,
    token_namechanger
)

from WebhookModules import (
    wb_deleter,
    wb_spammer,
    wb_namechanger
)

from MiscModules import (
    misc_inviteinfo,
    misc_gcnamechanger
)

class ModuleManager():
    def __init__(self) -> None:
        pass

    token_modules = [
        token_cspammer.channel_spammer,
        token_joiner.joiner_menu,
        token_checker.token_checker,
        token_ruleaccept.accept_rules,
        token_formatter.formatter,
        token_serverchecker.server_checker,
        token_scraper.scraper,
        token_biochanger.bio_changer,
        token_namechanger.name_changer
    ]

    webhook_modules = [
        wb_deleter.hdeleter,
        wb_spammer.hspammer_menu,
        wb_namechanger.hnamechanger
    ]

    misc_modules = [
        misc_inviteinfo.invite_info,
        misc_gcnamechanger.gcnamechanger
    ]
    
    async def select_module(self, hydra_self, type: str, modulo: int) -> None:
       match type:
           case "tokens":
            try:
                await self.token_modules[modulo-1](hydra_self)
            except Exception as e:
                self.cmessage(e)
                input()
           case "webhooks":
            try:
                await self.webhook_modules[modulo-1](hydra_self)
            except Exception as e:  
                self.cmessage(e)	
                input()
           case "misc":
            try:
                await self.misc_modules[modulo-1](hydra_self)
            except Exception as e:  
                self.cmessage(e)	
                input() 

    async def gheaders(self,channel_id:int,request_type:str,token:str) -> dict:
        """Generates new headers, in progress has async conflict issues with the better version"""

        def super_properties() -> dict:
            return {
                "os": "Windows",
                "browser": "Discord Client",
                "release_channel": "stable",
                "client_version": "1.0.9169",
                "client_version": "1.0.9174",
                "os_version": "10.0.19045",
                "system_locale": "en",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9169 Chrome/128.0.6613.36 Electron/32.0.0 Safari/537.36",
                "browser_version": "32.0.0",
                "client_build_number": 342408,
                "native_build_number": 54876,
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9174 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36",
                "browser_version": "32.2.7",
                "client_build_number": 353304,
                "native_build_number": 56336,
                "client_event_source": None,
            }

        self.cookies = self.getcookies
        #Reminder to automate getting Electron, Discord and Chrome user agent versions
        headers =  {
                    ":authority": "discord.com",
                    ":method": request_type,
                    ":scheme": "https",
                    "cookie": self.cookies,
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en-US,cs;q=0.9",
                    "Authorization": token,
                    "Priority": "u=1, i",
                    "Referer": "https://discord.com/",
                    "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9174 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36",
                    "X-Debug-Options": "bugReporterEnabled",
                    "X-Discord-Locale": "en-US",
                    "X-Discord-Timezone": "America/New_York",
                    "x-super-properties": super_properties(),
                }
        
        headers[":path"] = f"api/v9/channels/{channel_id}/messages"
        return headers

    async def getcookies(self) -> str:
        """Tries to get cookies (no that cookie isnt mine)"""
        try:
            response = requests.get(
                "https://discord.com",
            )
            match response.status_code:
                case 200:
                    return "; ".join(
                        [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                    ) + "; locale=en-US"
                case _:
                    self.cmessage(f"\n| Failed to get cookies using Static")
                    return "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=62f9e16100a211ef8089eda5bffbf7f98e904ba04346eacdf57ee4af97bdd94e4c16f7df1db5132bea9132dd26b21a2a; __cfruid=a2ccd7637937e6a41e6888bdb6e8225cd0a6f8e0-1714045775; _cfuvid=s_CLUzmUvmiXyXPSv91CzlxP00pxRJpqEhuUgJql85Y-1714045775095-0.0.1.1-604800000; locale=en-US"
        except Exception as e:
            self.cmessage(f"\n| Error getting cookies >>: {e}")

    async def cproxy(self,type:str) -> None:
        """Dependacy for load_proxies"""
        try:
            with open("Data/proxies.txt","r+") as proxies:
                proxies.seek(0)
                lproxies = proxies.readlines()
                for line in lproxies:
                    line = line.strip()
                    if not line.startswith(type):
                        self.proxylist.append(type+line)
                    else:
                        self.proxylist.append(line)
        except Exception:
            self.cmessage(f"\n| Error >>: {Exception}")

    async def load_proxies(self) -> None:
        """Fixes proxies text (Ex. 127.8.3.4:8080 to http://127.8.3.4:8080)"""
        with open("config.json","r+") as config:
            fconfig = json.load(config)
            match fconfig["proxy_type"].upper():
                case "HTTP":
                    config.close()
                    self.cproxy("http://")
                case "SOCKS4":
                    config.close()
                    self.cproxy("socks4://")
                case "SOCKS5":
                    config.close()
                    self.cproxy("socks5://")
                case _:
                    self.cmessage("| Proxy Type not specified. Please change in the config!")
                    input()
                    self.menu()

        with open("config.json","r+") as config:
            config = json.load(config)
            self.proxytype = config["proxy_type"]
        
    async def schecker(self, server_id: int) -> None:
        async with aiohttp.ClientSession() as session:
            for token in self.tokens:
                with open(f"Data/Token_Checks/SIDC_{server_id}.txt","w+") as f:
                    async with session.get(
                        f"https://discord.com/api/v9/guilds/{server_id}",
                          headers={"authorization": token}
                          ) as response:
                        match response.status:
                            case 204:
                                f.write(token)
                            case 200:
                                f.write(token)
