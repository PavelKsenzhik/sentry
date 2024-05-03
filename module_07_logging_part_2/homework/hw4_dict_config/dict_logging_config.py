import logging.handlers
import logging

from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import LevelFileHandler


class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return str.isascii(record.msg)


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "level": "DEBUG",
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%I:%M:%S",
        }
    },
    "filters": {
        "ascii": {
            "()": ASCIIFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
            "filters": ["ascii"],
        },
        "multi_file_handler": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii"],
        },
        "time_rotating": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "when": "h",
            "interval": 10,
            "backupCount": 1,
            "filename": "utils.txt",
            "filters": ["ascii"],
        },
        'server_handler': {
            '()': logging.handlers.HTTPHandler,
            'host': '127.0.0.1:5000',
            'url': '/log',
            'method': 'POST',
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "multi_file_handler", "server_handler"],
        },
        "app.utils": {
            "level": "INFO",
            "handlers": ["time_rotating"],
        },
    }
}
