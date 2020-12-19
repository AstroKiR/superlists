#!/usr/bin/env python3

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import unittest


MAX_WAIT = 10
DRIVER_PATH = '/home/astrok/Documents/Python/projects/tdd/drivers/chromedriver'


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(DRIVER_PATH)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):

        # John visits the start page
        self.browser.get(self.live_server_url)

        # He notices the page title and header mantion to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do list straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item')

        # He types "Buy new tires"
        inputbox.send_keys('Buy new tires')

        # When he hits enter the page updates and he sees the '1: Buy new tires' as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new tires')

        # There is still a text box inviting his to add another item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item')

        # He enters "Change the tires"
        inputbox.send_keys('Change the tires')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and he sees two rows in to-do list
        # 1: Buy new tires
        # 2: Change the tires
        self.wait_for_row_in_list_table('1: Buy new tires')
        self.wait_for_row_in_list_table('2: Change the tires')

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # John visits the start page
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy new tires')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new tires')

        # He notices that his list has a unique URL
        john_list_url = self.browser.current_url
        self.assertRegex(john_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of John's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome(DRIVER_PATH)

        # Francis visits the home page. There is no sign of John's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new tires', page_text)
        self.assertNotIn('Change the tires', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, john_list_url)

        # Again, there is no trace of John's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new tires', page_text)
        self.assertNotIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep



if __name__ == '__main__':
    unittest.main(warnings='ignore')

