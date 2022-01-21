import discord
import yaml
import os

config_instances = {}


class ConfigDoesntExistError(Exception):
    pass


class ConfigNotLoadedError(Exception):
    pass


class Config:
    def __init__(self, identifier: str, create_new_file_if_absent: bool = True):
        config_instances[identifier] = self
        self.__data = {}
        self.__path = f"./config/{identifier}.yml"
        if not os.path.isfile(self.__path):
            if create_new_file_if_absent:
                self._write_config()
            else:
                raise ConfigDoesntExistError
        self._load_config()

    @property
    def data(self) -> dict:
        return self.__data

    def get(self, *args, **kwargs):
        """Shorthand for getting key from data"""
        return self.__data.get(*args, **kwargs)

    def _load_config(self) -> None:
        with open(self.__path, "r") as f:
            self.__data = yaml.safe_load(f) or {}

    def _write_config(self) -> None:
        with open(self.__path, "w") as f:
            yaml.safe_dump(self.__data, f)


def get_config(identifier: str, create_new_file_if_absent: bool = True, load_if_not_loaded: bool = True) -> Config:
    config = config_instances.get(identifier)
    if not config:
        if load_if_not_loaded:
            config = Config(identifier, create_new_file_if_absent)
        else:
            raise ConfigNotLoadedError
    return config


def get_config_discord_file(identifier: str) -> discord.File:
    path = f"./config/{identifier}.yml"
    return discord.File(path, filename=f"{identifier}.yml")
