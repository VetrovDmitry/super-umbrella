import unittest
import requests
import os


API_URL = ''
API_KEY = ''


class SignupCase(unittest.TestCase):
    ep_url = os.path.join(API_URL, 'signup')
    headers = {
        'X-API-Key': API_KEY
    }
    test_user = {
        'fullname': 'Test User1',
        'username': 'test_user_1',
        'sex': 'Male',
        'birth_date': '1970-01-01',
        'email': 'test1@test.com',
        'password': 'testtest'
    }

    def test_first_register(self):
        response = requests.post(self.ep_url, headers=self.headers, params=self.test_user)
        self.assertEqual(response.status_code, 201)  # add assertion here

    def test_second_register(self):
        response = requests.post(self.ep_url, headers=self.headers, params=self.test_user)
        self.assertEqual(response.status_code, 409)


class TokenCase(unittest.TestCase):
    ep_url = os.path.join(API_URL, 'token')
    headers = {
        'X-API-Key': API_KEY
    }
    right_creds = {
        "username": "test_user_1",
        "password": "testtest"
    }
    wrong_creds_1 = {
        "username": "test_user_2",
        "password": "testtest"
    }
    wrong_creds_2 = {
        "username": "test_user_1",
        "password": "nonononono"
    }

    def test_right_creds(self):
        response = requests.post(self.ep_url, headers=self.headers, params=self.right_creds)
        self.assertEqual(response.status_code, 202)

    def test_wrong_creds_1(self):
        response = requests.post(self.ep_url, headers=self.headers, data=self.wrong_creds_1)
        self.assertEqual(response.status_code, 401)

    def test_wrong_creds_2(self):
        response = requests.post(self.ep_url, headers=self.headers, data=self.wrong_creds_2)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
