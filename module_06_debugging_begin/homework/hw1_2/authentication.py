"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import getpass
import hashlib
import logging
import re
from typing import List

ENGLISH_WORDS_PATH = "./english_words.txt"


logger = logging.getLogger("password_checker")

english_words = set()

def get_english_words() -> set:
    global english_words

    if len(english_words) == 0:
        with open(ENGLISH_WORDS_PATH, 'r', encoding="utf-8") as file:
            for index, word in enumerate(file.readlines()):
                word = word.replace('\n', '')
                if len(word) > 4:
                    english_words.add(word)

    return english_words


def get_words_from_string(string: str) -> List[str]:
    return re.findall(r"\D{4,}", string.lower())


def is_strong_password(password: str) -> bool:
    eng_words = get_english_words()

    words = get_words_from_string(password.lower())

    for word in words:
        if word in eng_words:
            return True

    return False


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename='stderr.txt',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл неправильный пароль!")
    exit(1)
