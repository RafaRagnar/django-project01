import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # The user enters their username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # The user submits the form
        form.submit()

        # The user sees the login success message and their name
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # User opens login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User tries to send empty values
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # The user submits the form
        form.submit()

        # The user sees an error message on the screen
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User opens login page
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User tries to send values ​​with data that does not match
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # The user submits the form
        form.submit()

        # The user sees an error message on the screen
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
