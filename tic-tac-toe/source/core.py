"""Core of bot`s calculating"""

import random
from telegram.ext import ContextTypes
from config.base import GameConfig, TextConfig, ValidateStatus

from config.logger import Logger
logger = Logger().get_logger(__name__)


def choosing_algorithm(context: ContextTypes.DEFAULT_TYPE) -> int | tuple:
    """
    Algorithm to choose zero position (randomly)

    :param context: internal state with params
    :return:
        0 - no free positions or
        tuple - row, col of choosen position
    """

    board = context.user_data['keyboard_state']

    free_positions = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == GameConfig.FREE_SPACE:
                free_positions.append((row, col))

    if len(free_positions) == 0:
        logger.debug('No free positions.')
        return 0

    row, col = random.choice(free_positions)
    logger.debug(f'Chosen position is [{row, col}].')
    return row, col


def check_winner(fields: list[list[str]]) -> [TextConfig, list[tuple[int]]]:
    """
    Check if crosses or zeros have won the game

    :param fields: table with the game
    :return:
        winner of the game, coordinates of winning line
    """
    people = [TextConfig.USER_NAME, TextConfig.COMPUTER_NAME]
    points = [GameConfig.CROSS, GameConfig.ZERO]
    coords = []

    for person, point in zip(people, points):

        # Horizontal and Vertical winning
        for i in range(3):
            if fields[i][0] == fields[i][1] == fields[i][2] == point:
                logger.debug(f'Horizontal winning of {person}.')
                coords = [(i, 0), (i, 1), (i, 2)]
                return person, coords

            if fields[0][i] == fields[1][i] == fields[2][i] == point:
                logger.debug(f'Vertical winning of {person}.')
                coords = [(0, i), (1, i), (2, i)]
                return person, coords

        # Main diagonal won
        if fields[0][0] == fields[1][1] == fields[2][2] == point:
            logger.debug(f'Main diagonal won - {person}.')
            coords = [(0, 0), (1, 1), (2, 2)]
            return person, coords

        # Side diagonal won
        if fields[0][2] == fields[1][1] == fields[2][0] == point:
            logger.debug(f'Side diagonal won - {person}.')
            coords = [(0, 2), (1, 1), (2, 0)]
            return person, coords

    return TextConfig.NO_ONE_NAME, coords


def validate_position(fields: list[list[str]], row: int, col: int) -> (ValidateStatus, TextConfig):
    """
    Check if chosen position is correct

    :param fields: table with the game
    :param row: chosen row index
    :param col: chosen col index
    :return:
        ValidateStatus (Correct or Not) and Text of interaction
    """

    if fields[row][col] == GameConfig.CROSS:
        logger.debug('Incorrect query')
        return ValidateStatus.INCORRECT, TextConfig.WRONG_POINT_CROSS

    if fields[row][col] == GameConfig.ZERO:
        logger.debug('Incorrect query')
        return ValidateStatus.INCORRECT, TextConfig.WRONG_POINT_ZERO

    return ValidateStatus.CORRECT, TextConfig.CORRECT_MOVE
