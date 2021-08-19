import os
import re


class Config:
    try:
        BOT_TOKEN = os.environ["BOT_TOKEN"]
    except KeyError:
        raise KeyError("Envionment variable BOT_TOKEN is not defined")

    DATABASE_URI = "postgresql://admin:admin@localhost/bot_db"
