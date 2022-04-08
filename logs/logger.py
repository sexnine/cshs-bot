from os import getcwd
import logging

path = getcwd() + "/logs/bot.log"
logging.basicConfig(path, level=logging.INFO, format='%(asctime)s - [%(levelname)s]: %(message)s')

class Logger:
    def __init__(self, s):
        self.s = s

    def start(self):
        logging.info(f"Cog {self.s} has been initialized.")

    def info(self, message):
        logging.info(f"Logged in cog {self.s.__qualname__}: {message}")

    def debug(self, message):
        logging.debug(f"Logged in cog {self.s.__qualname__}: {message}")

    def warning(self, message):
        logging.debug(f"Logged in cog {self.s.__qualname__}: {message}")

    def error(self, message, ctx):
        logging.debug(f"An error occurred in cog {self.s.__qualname__} in command {ctx.command}: {message}")

    def __del__(self):
        logging.debug(f"Cog {self.s.__qualname__} has been uninitialized.")
