from datetime import datetime
from unittest import TestCase
from freezegun import freeze_time
from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app, GREETINGS


class TestHelloWorld(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    @freeze_time('2024-01-24')
    def test_can_get_correct_weekdate(self):
        username = 'Pavel'
        weekday = datetime.today().weekday()
        greeting = GREETINGS[weekday]
        test_str = f'Привет, {username}. {greeting}!'

        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertEqual(test_str, response_text)
