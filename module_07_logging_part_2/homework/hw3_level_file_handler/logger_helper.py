import logging


class LevelFileHandler(logging.Handler):
    def __init__(self, name='app', level='DEBUG', mode='a') -> None:
        super().__init__(level)
        self._mode = mode
        self._name = name

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(f"./calc_{record.levelname.lower()}.log", mode=self._mode) as f:
            f.write(message + "\n")


def get_logger(name):
    logger = LevelFileHandler(name)

    return logger
