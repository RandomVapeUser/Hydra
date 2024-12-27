import os

async def formatter(self) -> None:
        self.clear()
        self.send_logo()
        self.cmessage(f"\n| [Path to File] >>: ",True)
        path = input().strip()

        if not os.path.isfile(path):
            self.cmessage("\n| [Error] >>> Invalid Path!")
            input()
            await self.Hydra.main.menu()

        tokens = []
        fpath = os.path.join(os.path.dirname(path), "/Data/Token_Checks/Formated_Tokens.txt")

        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    tokens.append(parts[2])

        with open(fpath, 'w') as f:
            for token in tokens:
                f.write(token + '\n')

        self.cmessage("\n| Saved tokens to /Data/Token_Checks/Formated_Tokens.txt")
        self.cmessage("| Add formated tokens? (Y/N) \n| >>: ",True)
        choice = input()

        if choice.upper().startswith("Y"):
            with open("tokens.txt","a+") as token_file:
                for i in tokens:
                    final_token = i.strip()
                    token_file.write(f"{final_token}\n")
        
        self.cmessage("| Successfully Added tokens!",True)
        input()
        await self.Hydra.main.menu()