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
    def __init__(self):
        init()
        self.start()
    
    # detects when logger has been initialized
    def start(self, cog_name):
        logging.info(f"Cog {cog_name} has been initialized.")
    
    # create the logging functions
    def info(self, cog_name, message):
        logging.info(f"Logged in cog {cog_name}: {message}")

    def debug(self, cog_name, message):
        logging.debug(f"Logged in cog {cog_name}: {message}")

    def warning(self, cog_name, message):
        logging.warning(f"Logged in cog {cog_name}: {message}")

    def error(self, cog_name, message, name):
        logging.error(f"An error occurred in cog {cog_name} in command {name}: {message}")
    
    # detect when logger has been uninitialized
    def __del__(self, cog_name):
        logging.debug(f"Cog {cog_name} has been uninitialized.")


class CogErrorLogging(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = Logger()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        command = ctx.command
        self.logger.error(command.cog_name, error, command)

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.logger.info(ctx.command.cog_name, f"{ctx.command} has been invoked.")
