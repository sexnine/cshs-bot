# importing modules
from os import getcwd
from time import time
import logging

# config the logging module
path = getcwd() + "/logs"
logging.basicConfig(filename=path + "current.log", level=logging.INFO, format='%(asctime)s - [%(levelname)s]: %(message)s')

def init():
    with open(path + "current.log", "r") as f:
        data = f.read()
        with open(path + "current.log", "w") as f1:
            if data != "":
                ts = data.split("\n")[0]
                print(ts)
                with open(path + f"{ts}.log", "w") as file:
                    file.write(data)
            f1.write(str(int(time())) + "\n")


# implementing the logger class
class Logger:
    def __init__(self, s):
        self.s = s
        self.start()
    
    # detects when logger has been initialized
    def start(self):
        logging.info(f"Cog {self.s} has been initialized.")
    
    # create the logging functions
    def info(self, message):
        logging.info(f"Logged in cog {self.s.__class__.__name__}: {message}")

    def debug(self, message):
        logging.debug(f"Logged in cog {self.s.__class__.__name__}: {message}")

    def warning(self, message):
        logging.warning(f"Logged in cog {self.s.__class__.__name__}: {message}")

    def error(self, message, name):
        logging.error(f"An error occurred in cog {self.s.__class__.__name__} in command {name}: {message}")
    
    # detect when logger has been uninitialized
    def __del__(self):
        logging.debug(f"Cog {self.s.__class__.__name__} has been uninitialized.")