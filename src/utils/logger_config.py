import logging

LOGGING_FILE_NAME = 'app_server.log'
FORMATTING_STRING = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LEVEL = logging.INFO


class Logger(object):

    __initialized = False

    @classmethod
    def get_logger(cls, name):
        if not cls.__initialized:
            logging.basicConfig(
                filename=LOGGING_FILE_NAME,
                format=FORMATTING_STRING,
                level=LOGGING_LEVEL
            )
            cls.__initialized = True
            logging.getLogger("logger config").info("Logger has been configured")
        return logging.getLogger(name)

    def __init__(self, name):
        self._logger = Logger.get_logger(name)

    def info(self, message):
        self._logger.info(message)

    def error(self, message):
        self._logger.exception(message)

    def debug(self, message):
        self._logger.debug(message)

    def warning(self, message):
        self._logger.warning(message)

