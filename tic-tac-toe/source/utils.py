"""Simple utils to create keyboard"""

from copy import deepcopy
from config.base import DEFAULT_STATE
from config.logger import Logger
from telegram import InlineKeyboardButton

logger = Logger().get_logger(__name__)


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic-tac-toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[row][col], callback_data=f'{row}{col}')
            for col in range(3)
        ]
        for row in range(3)
    ]
