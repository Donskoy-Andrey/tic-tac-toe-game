"""Logging stuff"""

import logging
from config.base import LoggerConfig


class Logger:
    """Custom Logger class"""
    @staticmethod
    def _get_file_handler():
        """Provide log to file"""
        file_handler = logging.FileHandler(LoggerConfig.LOGGER_FILENAME)
        file_handler.setLevel(LoggerConfig.LOGGER_FILE_LEVEL)
        file_handler.setFormatter(
            logging.Formatter(
                LoggerConfig.LOGGER_FORMATTER,
                datefmt=LoggerConfig.DATETIME_FORMAT,
            )
        )
        return file_handler

    @staticmethod
    def _get_stream_handler():
        """Provide log to console"""
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LoggerConfig.LOGGER_STREAM_LEVEL)
        stream_handler.setFormatter(
            logging.Formatter(
                LoggerConfig.LOGGER_FORMATTER,
                datefmt=LoggerConfig.DATETIME_FORMAT,
            )
        )
        return stream_handler

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get logger instance based on file name

        :param name: file `__name__` variable
        """
        logging.basicConfig(
            handlers=[
                self._get_file_handler(),
                self._get_stream_handler(),
            ],
            level=logging.DEBUG,
        )

        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('httpcore').setLevel(logging.WARNING)
        logger = logging.getLogger(name)
        return logger
