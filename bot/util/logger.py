# importing modules
from discord.ext import commands
from os import getcwd
from time import time
import logging

# config the logging module
path = getcwd() + "/logs"
logging.basicConfig(filename=path + "/current.log", level=logging.INFO, format='%(asctime)s - [%(levelname)s]: %(message)s')

def init():
    with open(path + "/current.log", "r") as f:
        data = f.read()
    with open(path + "/current.log", "w+") as f:
        print(data)
        if data != "":
            timestamp = data.split("\n")[0]
            print(timestamp)
            with open(path + f"{timestamp}.log", "w") as file:
                file.write(data)
        f.write(str(int(time())) + "\n")

# implementing the logger class
class Logger:
    def __init__(self, cog_self):
        self.cog_self = cog_self
        self.cog_name = self.cog_self.__class__.__name__
        init()
        self.start()
    
    # detects when logger has been initialized
    def start(self):
        logging.info(f"Cog {self.cog_name} has been initialized.")
    
    # create the logging functions
    def info(self, message):
        logging.info(f"Logged in cog {self.cog_name}: {message}")

    def debug(self, message):
        logging.debug(f"Logged in cog {self.cog_name}: {message}")

    def warning(self, message):
        logging.warning(f"Logged in cog {self.cog_name}: {message}")

    def error(self, message, name):
        logging.error(f"An error occurred in cog {self.cog_name} in command {name}: {message}")
    
    # detect when logger has been uninitialized
    def __del__(self):
        logging.debug(f"Cog {self.cog_name} has been uninitialized.")


class CogErrorLogging(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = Logger(self)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        self.logger.error(error, ctx)

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.logger.info(f"{ctx.command} has been invoked.")
