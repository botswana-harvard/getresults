import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User


class BaseSeleniumTest(StaticLiveServerTestCase):

    username = 'melissa'
    password = '123'
    email = 'm@123.org'

    def setUp(self):
        User.objects.create_superuser(self.username, self.email, self.password)
        super().setUp()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def login(self):
        username = self.browser.find_element_by_name('username')
        username.send_keys(self.username)
        userpwd = self.browser.find_element_by_name('password')
        userpwd.send_keys(self.password)
        userpwd.send_keys(Keys.RETURN)

    def navigate_to_admin(self):
        self.browser.get(self.live_server_url + '/admin/')

    def navigate_to_admin_getresults_patient(self):
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Getresults_Patient', body.text)
        self.browser.find_element_by_link_text('Getresults_Patient').click()

    def switch_to_new_window(self, text_in_element, element_id):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                element = self.browser.find_element_by_id(element_id)
                if text_in_element in element.text:
                    return
            retries -= 1
            time.sleep(0.5)
