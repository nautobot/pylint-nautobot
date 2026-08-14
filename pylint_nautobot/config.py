"""Config module to load settings."""

# pylint: disable=no-name-in-module
import sys
from pathlib import Path
from typing import List, Optional

import toml
from pydantic.error_wrappers import ValidationError
from pydantic.networks import AnyHttpUrl, IPvAnyAddress, IPvAnyNetwork
from pydantic.types import DirectoryPath, FilePath, SecretStr
from pydantic_settings import BaseSettings

SETTINGS = None
ENV_FILE_PATH = Path(__file__) / ".." / ".." / ".env"


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Main Settings Class for the project.

    The type of each setting is defined using Python annotations and Pydantic field types
    and is validated when a config file is loaded with Pydantic.
    """

    string_required: str
    secret_optional: Optional[SecretStr]  # pylint: disable=unsubscriptable-object
    array_default: List[str] = []
    url_default: AnyHttpUrl = "http://localhost"
    ip_address: IPvAnyAddress = "192.168.0.1"
    ip_network: IPvAnyNetwork = "2001:db8:3c4d:15::/64"
    file: FilePath = "some/path/file.txt"
    directory: DirectoryPath = "tests/"

    class Config:  # pylint: disable=too-few-public-methods
        """Config class to be used for Settings."""

        env_prefix = "PYLINT_NAUTOBOT"
        env_file = ENV_FILE_PATH.resolve()
        env_file_encoding = "utf-8"


def load(config_file_name="pyproject.toml", config_data=None):
    """Loads passed dynamic settings data using `config data` or from a TOML configuration file (pyproject.toml).

    When loaded from file, the settings for this app are expected to be in [tool.pylint-nautobot] in TOML
    if nothing is found in the config file or if the config file do not exist, the default values will be used.

    Args:
        config_file_name (str, optional): Name of the configuration file to load. Defaults to "pyproject.toml".
        config_data (dict, optional): dict to load as the config file instead of reading the file. Defaults to None.
    """
    global SETTINGS  # pylint: disable=global-statement

    # Load settings from dynamically passed data
    if config_data:
        SETTINGS = Settings(**config_data)

    # Or load from configuration file
    else:
        config_file = Path(config_file_name)

        if config_file.exists():
            config_tmp = toml.loads(config_file.read_text(encoding="UTF-8"))

            if "tool" in config_tmp and "pylint_nautobot" in config_tmp.get("tool", {}):
                SETTINGS = Settings(**config_tmp["tool"]["pylint_nautobot"])

    # If no config loaded, used defaults
    if SETTINGS is None:
        SETTINGS = Settings()

    return SETTINGS


def load_or_exit(config_file_name="pyproject.toml", config_data=None):
    """Loads passed dynamic settings data using `config data` or from a TOML configuration file (pyproject.toml).

    If a validation error is found, it will print out the respective error and exit from the app.

    When loaded from file, the settings for this app are expected to be in [tool.pylint_nautobot] in TOML
    if nothing is found in the config file or if the config file do not exist, the default values will be used.

    Args:
        config_file_name (str, optional): Name of the configuration file to load. Defaults to "pyproject.toml".
        config_data (dict, optional): dict to load as the config file instead of reading the file. Defaults to None.
    """
    try:
        load(config_file_name=config_file_name, config_data=config_data)
    except ValidationError as err:
        print(f"Configuration not valid, found {len(err.errors())} error(s)")
        for error in err.errors():
            print(f"  {'/'.join(error['loc'])} | {error['msg']} ({error['type']})")
        sys.exit(1)
