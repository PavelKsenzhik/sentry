import datetime
from unittest import TestCase
from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(TestCase):
    def setUp(self):
        self.name = 'Pavel'
        self.year_of_birth = 2000
        self.address = 'Panchenko'

        self.student = Person(self.name, self.year_of_birth, self.address)

    def test_get_age(self):
        now = datetime.datetime.now()
        age = now.year - self.year_of_birth
        self.assertEqual(age, self.student.get_age())

    def test_get_name(self):
        self.assertEqual(self.name, self.student.get_name())

    def test_set_name(self):
        name = 'Mark'
        self.student.set_name(name)
        self.assertEqual(name, self.student.name)

    def test_set_address(self):
        address = 'Lastoch'
        self.student.set_address(address)
        self.assertEqual(address, self.student.address)

    def test_is_homeless(self):
        address = ''
        self.student.set_address(address)
        self.assertTrue(self.student.is_homeless())

    def test_is_not_homeless(self):
        address = 'Lastoch'
        self.student.set_address(address)
        self.assertFalse(self.student.is_homeless())
