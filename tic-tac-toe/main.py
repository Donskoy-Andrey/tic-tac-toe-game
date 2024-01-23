"""Entry point for the bot"""

from telegram import Update
from telegram.ext import (
    Application, CallbackQueryHandler, CommandHandler, ConversationHandler
)
from config.base import GameConfig
from config.logger import Logger
from source.bot import start, game

logger = Logger().get_logger(__name__)


def main() -> None:
    """Run the bot"""

    logger.info('Start the bot.')
    application = Application.builder().token(GameConfig.TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GameConfig.PLAY: [
                CallbackQueryHandler(game, pattern='^' + f'{row}{col}' + '$')
                for row in range(3) for col in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],

    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info('Finalize the bot.')


if __name__ == '__main__':
    main()
