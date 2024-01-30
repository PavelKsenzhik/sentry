"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
import unittest
from hw1_registration import app


class TestAccounting(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.reg_url = '/registration'
        self.form_data = {
            'email': 'Test@mail.ru',
            'phone': 1234567891,
            'name': 'Pavel',
            'address': 'Address 16',
            'index': 220019,
            'comment': 'Comment 16',
        }

    def test_reg_full(self):
        data = self.form_data
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)

    # Test Email
    def test_reg_email(self):
        data = self.form_data
        data['email'] = 'test@mail.ru'
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)
        self.assertIn(str(self.form_data['email']), response_text)

    def test_reg_no_email(self):
        data = self.form_data
        del data['email']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response_text)
        self.assertIn('This field is required', response_text)

    def test_reg_wrong_email(self):
        data = self.form_data
        data['email'] = 'asddsa'
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response_text)
        self.assertIn('Invalid email address', response_text)

    # Test Phone
    def test_reg_phone(self):
        data = self.form_data
        data['phone'] = 9876543219
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)
        self.assertIn(str(self.form_data['phone']), response_text)

    def test_reg_wrong_phone(self):
        data = self.form_data
        data['phone'] = 123
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input', response_text)
        self.assertIn('phone', response_text)

    def test_reg_no_phone(self):
        data = self.form_data
        del data['phone']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response_text)
        self.assertIn('This field is required', response_text)

    # Test Name
    def test_reg_name(self):
        data = self.form_data
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)

    def test_reg_no_name(self):
        data = self.form_data
        del data['name']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response_text)
        self.assertIn('This field is required', response_text)

    # Test Address
    def test_reg_address(self):
        data = self.form_data
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)

    def test_reg_no_address(self):
        data = self.form_data
        del data['address']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('address', response_text)
        self.assertIn('This field is required', response_text)

    # Test Index
    def test_reg_index(self):
        data = self.form_data
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)

    def test_reg_no_index(self):
        data = self.form_data
        del data['index']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 400)
        self.assertIn('index', response_text)
        self.assertIn('This field is required', response_text)


    # Test Comment
    def test_reg_comment(self):
        data = self.form_data
        data['comment'] = 'test comment'
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)

    def test_reg_no_comment(self):
        data = self.form_data
        del data['comment']
        response = self.app.post(self.reg_url, data=data)
        response_text = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user', response_text)


if __name__ == '__main__':
    unittest.main()
