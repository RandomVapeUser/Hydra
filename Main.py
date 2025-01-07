from Hydra import Hydra
import asyncio

#Start
async def start():
    hydra = Hydra.Main()
    await hydra.menu()

if __name__ == "__main__":
    asyncio.run(start())
