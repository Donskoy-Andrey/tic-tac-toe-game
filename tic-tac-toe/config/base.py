"""Base classes for bot"""

import os
import logging
from enum import Enum
from dataclasses import dataclass
from dotenv import load_dotenv

# Load secrets
load_dotenv()


@dataclass
class GameConfig:
    """Constants for the game"""

    TOKEN = os.environ.get('BOT_FATHER_TOKEN')

    FREE_SPACE = '⋅'
    CROSS = '✘'
    ZERO = '●'
    CROSS_WINNER = '❎'
    ZERO_WINNER = '🟢'
    PLAY = True


DEFAULT_STATE = [
    [GameConfig.FREE_SPACE for _ in range(3)]
    for _ in range(3)
]


@dataclass
class LoggerConfig:
    """Constants for the logger"""

    LOGGER_STREAM_LEVEL = logging.DEBUG
    LOGGER_FILE_LEVEL = logging.DEBUG
    DATETIME_FORMAT = "%Y-%M-%d %H:%M:%S"
    LOGGER_FILENAME = "data/tic-tac-toe.log"
    LOGGER_FORMATTER = "[%(asctime)-19s] %(levelname)-8s : [%(name)s] : %(message)s"


@dataclass
class TextConfig:
    """Texts for the game"""

    DEFAULT_TEXT = f'Your turn! Please, put {GameConfig.CROSS} to the free place'

    WRONG_POINT_ZERO = 'It is my point! Do not touch it!'
    WRONG_POINT_CROSS = 'You have already put cross here! Choose another one.'
    CORRECT_MOVE = 'It is correct move.'

    DRAW = 'It is a draw. Thank you for the game!'
    COMPUTER_WON = 'I won! You are an absolute LOSER!'
    USER_WON = 'You won! Congratulations...'

    USER_NAME = 'USER'
    COMPUTER_NAME = 'COMPUTER'
    NO_ONE_NAME = 'NO ONE'

    FINAL_TEXT = 'To start a new game, use /start command.'


class ValidateStatus(Enum):
    """Correct move or not"""
    CORRECT = 1
    INCORRECT = 0
