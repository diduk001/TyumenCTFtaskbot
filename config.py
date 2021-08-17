import os
from sqlalchemy import create_engine

class Config:
    # Bot Token
    try:
        BOT_TOKEN = os.environ["BOT_TOKEN"]
    except KeyError:
        raise KeyError("Envionment variable BOT_TOKEN is not defined")

    # DATABASE = "mongodb:///?Server=127.0.0.1&;Port=27017&Database=bot_db"
    # engine = create_engine(DATABASE)