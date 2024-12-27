import threading
import websocket
import json
import time
import sys
import os

cwd = os.getcwd()
parent_dtr = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(parent_dtr)
from Modules import TextAssets as assets
from Hydra import Hydra

class Utils:
    """Utils for ID scraper"""
    @staticmethod
    def range_corrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    @staticmethod
    def get_ranges(index, multiplier, member_count):
        initial_num = int(index * multiplier)
        ranges = [[initial_num, initial_num + 99]]
        if member_count > initial_num + 99:
            ranges.append([initial_num + 100, initial_num + 199])
        return Utils.range_corrector(ranges)

    @staticmethod
    def parse_member_list_update(response):
        try:
            data = response["d"]
            member_data = {
                "online_count": data["online_count"],
                "member_count": data["member_count"],
                "id": data["id"],
                "guild_id": data["guild_id"],
                "hoisted_roles": data["groups"],
                "types": [op["op"] for op in data["ops"]],
                "locations": [],
                "updates": [],
            }

            for chunk in data["ops"]:
                op_type = chunk["op"]
                if op_type in {"SYNC", "INVALIDATE"}:
                    member_data["locations"].append(chunk["range"])
                    member_data["updates"].append(chunk["items"] if op_type == "SYNC" else [])
                elif op_type in {"INSERT", "UPDATE", "DELETE"}:
                    member_data["locations"].append(chunk["index"])
                    member_data["updates"].append(chunk["item"] if op_type != "DELETE" else [])

            return member_data
        except KeyError as e:
            print(f"KeyError in parsing: {e}")
            return None
        
class DiscordSocket(websocket.WebSocketApp):
    """Discord Websocket for scraping user IDS"""
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.blacklisted_ids = {
            "1100342265303547924", "1190052987477958806", 
            "833007032000446505", "1287914810821836843", "1273658880039190581"
        }
        self.end_scraping = False
        self.guilds = {}
        self.members = {}
        self.ranges = [[0, 0]]
        self.last_range = 0
        self.packets_recv = 0

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0.0.0 Safari/537.36"),
        }

        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
        )

    def run(self):
        self.run_forever()
        return self.members

    def scrape_users(self):
        if not self.end_scraping:
            self.send(json.dumps({
                "op": 14,
                "d": {
                    "guild_id": self.guild_id,
                    "typing": True,
                    "activities": True,
                    "threads": True,
                    "channels": {self.channel_id: self.ranges}
                }
            }))

    def on_open(self, ws):
        self.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows NT",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "it-IT",
                    "browser_user_agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                                           "Chrome/126.0.0.0 Safari/537.36"),
                    "browser_version": "126.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 311885,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))

    def heartbeat_thread(self, interval):
        while not self.end_scraping:
            try:
                self.send(json.dumps({"op": 1, "d": self.packets_recv}))
                time.sleep(interval)
            except Exception as e:
                print(f"Error during heartbeat: {e}")
                break

    def on_message(self, ws, message):
        try:
            decoded = json.loads(message)
            if not decoded:
                return

            if decoded["op"] != 11:
                self.packets_recv += 1

            if decoded["op"] == 10:
                threading.Thread(
                    target=self.heartbeat_thread,
                    args=(decoded["d"]["heartbeat_interval"] / 1000,),
                    daemon=True,
                ).start()

            if decoded["t"] == "READY":
                self.guilds.update({guild["id"]: {"member_count": guild["member_count"]} for guild in decoded["d"]["guilds"]})

            if decoded["t"] == "READY_SUPPLEMENTAL":
                self.ranges = Utils.get_ranges(0, 100, self.guilds[self.guild_id]["member_count"])
                self.scrape_users()

            elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
                parsed = Utils.parse_member_list_update(decoded)
                if parsed and parsed["guild_id"] == self.guild_id:
                    self.process_updates(parsed)
        except Exception as e:
            assets.AsciiAssets.cmessage("\n| Failed to Scrape ids (Check if the user is in the server).")
            exit = input()
            Hydra.main.menu()

    def process_updates(self, parsed):
        try:
            if "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]:
                for i, update_type in enumerate(parsed["types"]):
                    if update_type == "SYNC":
                        if not parsed["updates"][i]:
                            self.end_scraping = True
                            break
                        self.process_members(parsed["updates"][i])
                    elif update_type == "UPDATE":
                        self.process_members(parsed["updates"][i])

                    self.last_range += 1
                    self.ranges = Utils.get_ranges(self.last_range, 100, self.guilds[self.guild_id]["member_count"])
                    time.sleep(0.45)
                    self.scrape_users()

            if self.end_scraping:
                self.close()
        except Exception as e:
            print(f"Error processing updates: {e}")

    def process_members(self, updates):
        try:
            for item in updates:
                if "member" in item:
                    member = item["member"]
                    user_id = member["user"]["id"]
                    if user_id not in self.blacklisted_ids and not member["user"].get("bot"):
                        user_info = {
                            "tag": f"{member['user']['username']}#{member['user']['discriminator']}",
                            "id": user_id,
                        }
                        self.members[user_id] = user_info
        except Exception as e:
            print(f"Error processing members: {e}")

    def on_close(self, ws, close_code, close_msg):
        assets.AsciiAssets.cmessage(f"\n| Scraped {len(self.members)} members.")

    @staticmethod
    def scrape(token, guild_id, channel_id):
        sb = DiscordSocket(token, guild_id, channel_id)
        return sb.run()
    
    def member_scrape(self, guild_id, channel_id):
        global dnow
        members = DiscordSocket.scrape(self.token, guild_id, channel_id)
        
        os.makedirs("scraped", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"scraped/{guild_id}.txt"
        with open(filename, "w") as f:
            f.write("\n".join(members))