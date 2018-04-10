from selenium import webdriver
import time

driver = webdriver.Chrome('/Users/gaoyuan/MyStuff/webscrap/simplecrewler/chromedriver')
driver.get('http://www.google.com')
time.sleep(5)
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)
driver.quit()


import selenium.webdriver.chrome.service as service

service = service.Service('/Users/gaoyuan/MyStuff/webscrap/simplecrewler/chromedriver')
service.start()
capabilities = {'chrome.binary': '/Applications/Google Chrome.app'}
driver = webdriver.Remote(service.service_url, capabilities)
driver.get('http://www.google.com');
time.sleep(5) # Let the user actually see something!
driver.quit()