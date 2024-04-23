import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_zero_division__type_error(self):
        try:
            err_types = {ZeroDivisionError, TypeError}
            with BlockErrors(err_types):
                a = 1 / 0
        except:
            self.fail()

    def test_zero_division(self):
        with self.assertRaises(TypeError):
            err_types = {ZeroDivisionError}
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_outer_err_types(self):
        try:
            outer_err_types = {TypeError}
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except:
            self.fail()

    def test_err_types(self):
        try:
            err_types = {Exception}
            with BlockErrors(err_types):
                a = 1 / '0'
        except:
            self.fail()


if __name__ == '__main__':
    unittest.main()
