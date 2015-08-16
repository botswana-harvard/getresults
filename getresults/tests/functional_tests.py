from .base_selenium_test import BaseSeleniumTest


class TestInterface(BaseSeleniumTest):

    def test_admin(self):
        self.navigate_to_admin()
        self.login()
