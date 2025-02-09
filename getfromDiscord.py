import os
from dotenv import load_dotenv

load_dotenv()

DISCORDTOKEN = os.getenv("DISCORDTOKEN")

print(DISCORDTOKEN)