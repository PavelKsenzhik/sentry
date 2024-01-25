import json
from unittest import TestCase
from module_03_ci_culture_beginning.homework.hw3.accounting import app, storage


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

    def test_correct_add_endpoint(self):
        date = self.date
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        expected_value = self.sum

        response = self.add_data(date, self.sum)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_text, f'Текущее состояние {storage}')
        self.assertEqual(expected_value, storage[year][month][day])
        storage.clear()

    def test_invalid_date_add_endpoint(self):
        date = '20240d601'
        with self.assertRaises(ValueError):
            self.add_data(date, self.sum)

    def test_correct_calculate_year(self):
        self.add_data(self.date, self.sum)

        response = self.app.get(self.calculate_url + self.year)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{self.year} год: {self.sum}', response_text)
        storage.clear()

    def test_correct_calculate_year_month(self):
        self.add_data(self.date, self.sum)

        response = self.app.get(self.calculate_url + self.year + '/' + self.month)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{self.year} год {int(self.month)} месяц: {self.sum}', response_text)

    def test_correct_empty_storage_calculate_endpoint(self):
        year = '2023'
        response = self.app.get(self.calculate_url + year)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Данные за {year} год отсутствуют', response_text)