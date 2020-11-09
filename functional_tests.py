from selenium import webdriver


browser = webdriver.Chrome('/home/astrok/Documents/Python/projects/tdd/drivers/chromedriver')
browser.get('http://127.0.0.1:8000')

assert 'Django' in browser.title
