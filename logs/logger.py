from os import getcwd, listdir, remove
from os.path import splitext
from time import time
import logging

path = getcwd() + "/current.log"
logging.basicConfig(filename=path, level=logging.INFO, format='%(asctime)s - [%(levelname)s]: %(message)s')

with open("current.log", "r+") as f:
    data = f.read()
    if data != "":
        ts = f.readline(0)
        f.write("")
        with open(f"{ts}.log", "w") as file:
            file.write(time() + "\n" + data)

files = listdir()
logs = []
lowestlog = False
if len(files) > 11:
    for file in files:
        text = splitext(file)
        if text[1] == '.log':
            logs.append(int(text[0]))
    for log in logs:
        if not lowestlog or log > lowestlog:
            lowestlog = log

    remove(str(lowestlog) + ".log")


class Logger:
    def __init__(self, s):
        self.s = s
        self.start()

    def start(self):
        logging.info(f"Cog {self.s} has been initialized.")

    def info(self, message):
        logging.info(f"Logged in cog {self.s.__qualname__}: {message}")

    def debug(self, message):
        logging.debug(f"Logged in cog {self.s.__qualname__}: {message}")

    def warning(self, message):
        logging.warning(f"Logged in cog {self.s.__qualname__}: {message}")

    def error(self, message, ctx):
        logging.error(f"An error occurred in cog {self.s.__qualname__} in command {ctx.command}: {message}")

    def __del__(self):
        logging.debug(f"Cog {self.s.__qualname__} has been uninitialized.")
