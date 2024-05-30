import logging
import sys
from logging import getLogger

from colorama import Style, Fore

_default_log_format = "[%(levelname)s] %(asctime)s: %(message)s"

_logging_initialized = False


class ColorFormatter(logging.Formatter):
    FORMATS = {
            logging.DEBUG: f"{Fore.LIGHTBLUE_EX}{_default_log_format}{Style.RESET_ALL}",
            logging.INFO: f"{Fore.LIGHTGREEN_EX}{_default_log_format}{Style.RESET_ALL}",
            logging.WARNING: f"{Fore.LIGHTYELLOW_EX}{_default_log_format}{Style.RESET_ALL}",
            logging.ERROR: f"{Fore.LIGHTRED_EX}{_default_log_format}{Style.RESET_ALL}",
            logging.CRITICAL: f"{Fore.LIGHTRED_EX}{Style.BRIGHT}{_default_log_format}{Style.RESET_ALL}",
            }

    def format( self, record ):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def init_logging( debug: bool ):
    global _logging_initialized
    if _logging_initialized:
        return
    _logging_initialized = True
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter())
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[handler])


log = getLogger("ZigInstall")
