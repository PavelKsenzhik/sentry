import logging.config
import logging_tree

from module_07_logging_part_2.homework.hw4_dict_config.dict_logging_config import dict_config
from utils import string_to_operator

# logging_formatter = logging.Formatter(f"%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
#                                       datefmt='%I:%M:%S')
#
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(logging_formatter)
#
# multi_file_handler = get_logger("app")
# multi_file_handler.setFormatter(logging_formatter)
#
# logging.basicConfig(level='DEBUG', handlers=[stream_handler, multi_file_handler])

logging.config.dictConfig(dict_config)

logger = logging.getLogger("app")


def calc(args):
    logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.exception("Error while converting number 1", exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.exception("Error while converting number 1", exc_info=e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.debug(f"Result: {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")


def print_logs():
    with open('logging_tree.txt', mode='w') as file:
        file.write(logging_tree.format.build_description())


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2+3')

    # print_logs()
