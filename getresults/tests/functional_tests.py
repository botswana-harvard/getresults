import time

from .base_functional_tests import BaseFunctionalTest


class TestInterface(BaseFunctionalTest):

    def test_login(self):
        # Only authorized users can access the system
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys(self.username)
        self.browser.find_element_by_id('password').send_keys(self.password)
        self.browser.find_element_by_id('login').click()
        time.sleep(1)
        # self.assertIn('receive', self.browser.title.lower())
