from unittest import TestCase
from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestDecrypt(TestCase):
    def test_get_correct_decrypt_with_one_point(self):
        self.assertEqual(decrypt('абра-кадабра.'), 'абра-кадабра')
        self.assertEqual(decrypt('.'), '')

    def test_get_correct_decrypt_with_two_points(self):
        self.assertEqual(decrypt('абраа..-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра--..кадабра'), 'абра-кадабра')

    def test_get_correct_decrypt_with_any_points(self):
        self.assertEqual(decrypt('абраа..-.кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абрау...-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра........'), '')
        self.assertEqual(decrypt('абр......a.'), 'a')
        self.assertEqual(decrypt('1..2.3'), '23')
        self.assertEqual(decrypt('1.......................'), '')
