from redirect import Redirect
import sys
import io
import unittest
from contextlib import redirect_stdout, redirect_stderr


class RedirectTestCase(unittest.TestCase):
    def setUp(self):
        self.out_file = 'stdout.txt'
        self.err_file = 'stderr.txt'

        open(self.out_file, 'w').close()
        open(self.err_file, 'w').close()

    def test_redirect_stdout(self):
        stdout_file = open(self.out_file, 'w')
        with Redirect(stdout=stdout_file):
            print("Hello stdout.txt")
        stdout_file.close()

        with open(self.out_file, 'r') as file:
            result = file.read().strip()

        self.assertEqual(result, "Hello stdout.txt")

    def test_redirect_stderr(self):
        stderr_file = open(self.err_file, 'w')
        with Redirect(stderr=stderr_file):
            1 / 0
        stderr_file.close()

        with open(self.err_file, 'r') as file:
            result = file.read().strip()

        self.assertIn('ZeroDivisionError: division by zero', result)


if __name__ == '__main__':
    unittest.main()
