"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import re
from typing import List

all_words = set()
with open('/usr/share/dict/words', 'r') as word_file:
    all_words.update(set([i_word.lower().strip() for i_word in word_file]))

digit_letters = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}

digit_letters_revered = {}
for key, value in digit_letters.items():
    for i_letter in digit_letters[key]:
        digit_letters_revered[i_letter] = key


def change_word(word: str) -> str:
    new_word = ''.join(sorted([digit_letters_revered[i_char] for i_char in word if i_char in digit_letters_revered]))

    return new_word


def my_t9(input_numbers: str) -> List[str]:
    result = []

    digits = ''.join(sorted(re.sub('[^2-9]', '', input_numbers)))

    if len(digits) == 0:
        return []

    for i_word in all_words:
        if len(digits) == len(i_word) and digits == change_word(i_word):
            result.append(i_word)

    return result


if __name__ == '__main__':
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
