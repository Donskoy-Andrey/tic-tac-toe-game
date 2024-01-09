"""Base classes for bot"""

import os
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

# Load secrets
load_dotenv()


@dataclass
class GameConfig:
    """Constants for game"""

    TOKEN = os.environ.get('BOT_FATHER_TOKEN')

    FREE_SPACE = '.'
    CROSS = 'X'
    ZERO = 'O'
    CONTINUE_GAME = 0
    FINISH_GAME = 1


DEFAULT_STATE = [
    [GameConfig.FREE_SPACE for _ in range(3)]
    for _ in range(3)
]


@dataclass
class LoggerConfig:
    """Constants for logger"""

    LOGGER_STREAM_LEVEL = logging.DEBUG
    LOGGER_FILE_LEVEL = logging.DEBUG
    DATETIME_FORMAT = "%Y-%M-%d %H:%M:%S"
    LOGGER_FILENAME = "data/tic-tac-toe.log"
    LOGGER_FORMATTER = "[%(asctime)-19s] %(levelname)-8s : [%(name)s] : %(message)s"
