import unittest
from remote_execution import app

class TestRemoteExecution(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.code_url = '/run_code'
        self.data = {
            "code": 'print("test")',
            "timeout": 2,
        }

    def test_ok(self):
        data = self.data
        data["code"] = 'print("test_run_code")'
        response = self.app.post(self.code_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Python code successfully run', response_text)

    def test_low_timeout(self):
        data = self.data
        data["code"] = 'import time; print("test_low_timeout"); time.sleep(10); print("ended before timeout")'
        response = self.app.post(self.code_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Timeout ended", response_text)

    def test_invalid_code(self):
        data = self.data
        data["code"] = None

        response = self.app.post(self.code_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn("Ожидалась строка", response_text)

    def test_invalid_timeout(self):
        data = self.data
        data["timeout"] = -5

        response = self.app.post(self.code_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn("Ожидалось пооложительное число не больше 30", response_text)


if __name__ == '__main__':
    unittest.main()
