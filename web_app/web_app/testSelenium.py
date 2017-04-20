from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
# from django.conf import settings
# import os

class SeleniumTestCase(LiveServerTestCase):
	def setUp(self):
		# while True:
		# 	try:
		# 		self.selenium = chrome = webdriver.Remote(
		# 			command_executor='http://selenium:4444/wd/hub',
		# 			desired_capabilities=DesiredCapabilities.CHROME)
		# 		super(SeleniumTestCase, self).setUp()
		# 		break
		# 	except:
		# 		time.sleep(5)
		# 		continue
		self.selenium = chrome = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
		super(SeleniumTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(SeleniumTestCase, self).tearDown()

	def test_everything(self):
		selenium = self.selenium
		selenium.get('http://localhost:8000/')
		title = selenium.find_element_by_id('tasktic')
		self.assertEquals(title.text, "TaskTic")


