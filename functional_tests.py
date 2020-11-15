from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/home/astrok/Documents/Python/projects/tdd/drivers/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # A new user visits the start page
        self.browser.get('http://127.0.0.1:8000')

        # He notices the page title and header mantion to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do list straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Buy new tires"
        inputbox.send_keys('Buy new tires')

        # When he hits enter the page updates and he sees the '1: Buy new tires' as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy new tires' for row in rows))

        # There is still a text box inviting his to add another item. He enters "Change the tires"

        self.fail('Finish the test!')


        # The page updates again and he sees two rows in to-do list
        # 1: Buy new tires
        # 2: Change the tires

        # New use wonders whether the site will remember his list
        # Then he sees that the site has generated a unique URL for him -- there is some explanatory text to that effect

        # He visits that URL - his to-do list is still there.

        # The new user goes away from page


if __name__ == '__main__':
    unittest.main(warnings='ignore')
