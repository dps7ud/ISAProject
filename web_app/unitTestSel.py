from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import sys

class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://192.168.99.100:4444/wd/hub', 
            desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_example(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/')
        title = selenium.find_element_by_id('tasktic')
        self.assertEqual(title.text, "TaskTic")

    def test_top_user_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/')
        topUser = selenium.find_element_by_css_selector(".top-user")
        topUser.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/user'))

    def test_recent_task_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/')
        recentTask = selenium.find_element_by_css_selector(".recent-task")
        recentTask.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/task'))

    def test_user_page_to_task_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/user/1/')
        userTask = selenium.find_element_by_css_selector(".user-task")
        userTask.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/task'))

    def test_task_page_to_user_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/task/1/')
        userTask = selenium.find_element_by_css_selector(".task-user")
        userTask.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/user'))

    def test_task_page_to_review_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/task/1/')
        taskReview = selenium.find_element_by_css_selector(".task-review")
        taskReview.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/review'))

    def test_review_page_to_user_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/review/1/')
        reviewPoster = selenium.find_element_by_css_selector(".poster-user")
        reviewPoster.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/user'))

    def test_review_page_to_user_redirect(self):
        selenium = self.driver
        selenium.get('http://192.168.99.100:8000/review/1/')
        reviewTask = selenium.find_element_by_css_selector(".review-task")
        reviewTask.click()
        selenium.implicitly_wait(2)
        print(selenium.current_url)
        self.assertTrue(selenium.current_url.startswith('http://192.168.99.100:8000/task'))





    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()