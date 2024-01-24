import json
from unittest import TestCase
from module_03_ci_culture_beginning.homework.hw3.accounting import app


class TestAccounting(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.add_url = '/add/'
        self.calculate_url = '/calculate/'
        self.year = '2024'
        self.month = '01'
        self.day = '24'
        self.sum = 10
        self.date = self.year + self.month + self.day

    def add_data(self, date: str, number: int):
        url = f'{self.add_url}{date}/{number}'
        return self.app.get(url)

    def get_storage(self):
        return json.loads(self.app.get('/get-storage').data)

    def is_added_to_storage(self, date):
        year = str(int(date[:4]))
        month = str(int(date[4:6]))
        day = str(int(date[6:8]))

        storage = self.get_storage()

        if storage.get(year).get(month).get(day):
            return True
        else:
            return False

    def test_correct_add_endpoint(self):
        date = self.date

        self.add_data(date, self.sum)
        result = self.is_added_to_storage(date)

        self.assertTrue(result)

    def test_invalid_date_add_endpoint(self):
        date = '20240123'
        try:
            self.add_data(date, self.sum)
        except ValueError:
            self.assertRaises(ValueError)

    def test_correct_calculate_year(self):
        year = self.year
        response = self.app.get(self.calculate_url + year)
        response_text = response.data.decode()

        self.assertIn(f'{year} год: {self.sum}', response_text)

    def test_correct_calculate_year_month(self):
        year = self.year
        month = self.month

        response = self.app.get(self.calculate_url + year + '/' + month)
        response_text = response.data.decode()

        self.assertIn(f'{year} год {int(month)} месяц: {self.sum}', response_text)

    def test_correct_empty_storage_calculate_endpoint(self):
        year = '2023'
        response = self.app.get(self.calculate_url + year)
        response_text = response.data.decode()

        self.assertIn(f'Данные за {year} год отсутствуют', response_text)