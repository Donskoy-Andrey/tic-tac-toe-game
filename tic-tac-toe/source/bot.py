"""
Bot for playing tic-tac-toe game with multiple CallbackQueryHandlers.
"""

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from config.logger import Logger
from config.base import GameConfig, TextConfig, ValidateStatus
from source.utils import generate_keyboard, get_default_state
from source.core import choosing_algorithm, check_winner, validate_position

logger = Logger().get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Send message on `/start`.

    :param update: interaction with the user
    :param context: internal state with params
    :return:
        `Continue` code of the game
    """
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        TextConfig.DEFAULT_TEXT, reply_markup=reply_markup
    )
    return GameConfig.PLAY


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Main processing of the game.

    :param update: interaction with the user
    :param context: internal state with params
    :return:
        `End` or `Continue` code of the game
    """
    row, col = map(int, update.callback_query.data)

    # Validation
    status, message = validate_position(context.user_data['keyboard_state'], row, col)

    if status == ValidateStatus.INCORRECT:
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query.message.text != message:
            await update.callback_query.edit_message_text(
                message, reply_markup=reply_markup
            )
        return GameConfig.PLAY

    # User`s turn
    context.user_data['keyboard_state'][row][col] = GameConfig.CROSS
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)

    # Check winner after user`s turn
    winner, coords = check_winner(context.user_data['keyboard_state'])
    for possible_winner, text_winner in zip(
        [TextConfig.COMPUTER_NAME, TextConfig.USER_NAME],
        [TextConfig.COMPUTER_WON, TextConfig.USER_WON]
    ):
        if winner == possible_winner:
            await update.callback_query.edit_message_text(
                text_winner, reply_markup=reply_markup
            )
            return await end(update, context, coords)

    # Computer`s turn
    decision = choosing_algorithm(context)

    if decision == 0:
        # No free positions - it is a draw
        await update.callback_query.edit_message_text(
            TextConfig.DRAW, reply_markup=reply_markup
        )
        return await end(update, context)

    row, col = decision
    context.user_data['keyboard_state'][row][col] = GameConfig.ZERO
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)

    # Check winner after computer`s turn
    winner, coords = check_winner(context.user_data['keyboard_state'])
    for possible_winner, text_winner in zip(
        [TextConfig.COMPUTER_NAME, TextConfig.USER_NAME],
        [TextConfig.COMPUTER_WON, TextConfig.USER_WON]
    ):
        if winner == possible_winner:
            await update.callback_query.edit_message_text(
                text_winner, reply_markup=reply_markup
            )
            return await end(update, context, coords)

    return GameConfig.PLAY


async def end(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
    coords: list[tuple[int]] | None = None,
) -> int:
    """
    Returns `ConversationHandler.END`, which tells
    the ConversationHandler that the conversation is over.
    Draw winning positions.

    :param update: interaction with the user
    :param context: internal state with params
    :param coords: list of winning coordinates
    :return:
        `End` code of the game
    """
    if coords is None:
        coords = []

    if len(coords) > 0:
        # Drawing winning positions
        for (row, col) in coords:
            context.user_data['keyboard_state'][row][col] = (
                context
                .user_data['keyboard_state'][row][col]
                .replace(GameConfig.CROSS, GameConfig.CROSS_WINNER)
                .replace(GameConfig.ZERO, GameConfig.ZERO_WINNER)
            )

        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_reply_markup(reply_markup)

    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=TextConfig.FINAL_TEXT)
    return ConversationHandler.END
