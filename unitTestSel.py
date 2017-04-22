from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import sys

class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            #command_executor='http://192.168.99.100:4444/wd/hub', 
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.implicitly_wait(7)
        #self.address = 'http://192.168.99.100:8000'
        self.address = 'http://localhost:8000'
        self.auth = 'e1409c29a2833860a761821d53d703e32345dabaef9e3588f8755b0b2e133ad6'

    # def test_example(self):
    #     selenium = self.driver
    #     selenium.get(self.address)
    #     title = selenium.find_element_by_id('tasktic')
    #     self.assertEqual(title.text, "TaskTic")

    def test_button_redirects(self):
        selenium = self.driver
        selenium.get(self.address)
        
        #Test Home PAge -> Top User
        topUser = selenium.find_element_by_css_selector(".top-user")
        topUser.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('user_title')
        self.assertTrue(title.text.startswith('User'))
        
        # Test User Page -> Tasks associated with the user
        userTask = selenium.find_element_by_css_selector(".user-task")
        userTask.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('task_title')
        self.assertTrue(title.text.startswith('Task'))
        
        # Test Task Page -> reviews associated with the task
        taskReview = selenium.find_element_by_css_selector(".task-review")
        taskReview.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('review_title')
        self.assertTrue(title.text.startswith('Review'))
        
        # Test Review Page -> creator user of that review
        reviewPoster = selenium.find_element_by_css_selector(".poster-user")
        reviewPoster.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('user_title')
        self.assertTrue(title.text.startswith('User'))
        
        # Test main nav bar click to go to home page
        homeNav = selenium.find_element_by_id('homeNav')
        homeNav.click()
        title = selenium.find_element_by_id('tasktic')
        self.assertEqual(title.text, "TaskTic")
        
        # Test home page -> recent task
        recentTask = selenium.find_element_by_css_selector(".recent-task")
        recentTask.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('task_title')
        self.assertTrue(title.text.startswith('Task'))
        
        # Test task page -> users associated with the task
        userTask = selenium.find_element_by_css_selector(".task-user")
        userTask.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('user_title')
        self.assertTrue(title.text.startswith('User'))
        
        selenium.get(self.address + '/review/1/')
        reviewTask = selenium.find_element_by_css_selector(".review-task")
        reviewTask.click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('task_title')
        self.assertTrue(title.text.startswith('Task'))

    # def test_recent_task_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address)
    #     recentTask = selenium.find_element_by_css_selector(".recent-task")
    #     recentTask.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('task_title')
    #     self.assertTrue(title.text.startswith('Task'))

    # def test_user_page_to_task_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address + '/user/1/')
    #     userTask = selenium.find_element_by_css_selector(".user-task")
    #     userTask.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('task_title')
    #     self.assertTrue(title.text.startswith('Task'))

    # def test_task_page_to_user_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address + '/task/1/')
    #     userTask = selenium.find_element_by_css_selector(".task-user")
    #     userTask.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('user_title')
    #     self.assertTrue(title.text.startswith('User'))

    # def test_task_page_to_review_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address + '/task/1/')
    #     taskReview = selenium.find_element_by_css_selector(".task-review")
    #     taskReview.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('review_title')
    #     self.assertTrue(title.text.startswith('Review'))

    # def test_review_page_to_user_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address + '/review/1/')
    #     reviewPoster = selenium.find_element_by_css_selector(".poster-user")
    #     reviewPoster.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('user_title')
    #     self.assertTrue(title.text.startswith('User'))

    # def test_review_page_to_task_redirect(self):
    #     selenium = self.driver
    #     selenium.get(self.address + '/review/1/')
    #     reviewTask = selenium.find_element_by_css_selector(".review-task")
    #     reviewTask.click()
    #     selenium.implicitly_wait(2)
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('task_title')
    #     self.assertTrue(title.text.startswith('Task'))

    def test_login(self):
        selenium = self.driver
        selenium.get(self.address + '/login')
        selenium.find_element_by_id("username").send_keys('user1')
        selenium.find_element_by_id("pw").send_keys('m')
        selenium.find_element_by_id("submit_login").click()
        # try:
        #     title = WebDriverWait(selenium, 10).until(EC.presence_of_element_located((By.ID, "tasktic")))
        # finally:
        #     self.assertTrue(False, "Title Page never loaded")
        print(selenium.current_url)
        title = selenium.find_element_by_id('tasktic') 
        self.assertEqual(title.text, "TaskTic")
        logout = selenium.find_element_by_id('nav5')
        self.assertEqual(logout.text, "Logout")
        try:
            signup = selenium.find_element_by_id('nav4')
            self.assertTrue(False)
        except:
            self.assertTrue(True)
        self.assertEqual(selenium.find_element_by_id('nav6').text, 'Profile')
        self.assertEqual(selenium.find_element_by_id('nav8').text, 'Create Task')
        cookies = selenium.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'auth':
                logged_in = True
                break
        if not logged_in:
            self.assertTrue(False, "auth token not set")

    def test_need_login_redirect_profile_create_review(self):
        selenium = self.driver
        selenium.get(self.address + '/profile')
        print(selenium.current_url)
        title = selenium.find_element_by_id('login_title')
        self.assertTrue(title.text.startswith('Login'))
        selenium.find_element_by_id("username").send_keys('user1')
        selenium.find_element_by_id("pw").send_keys('m')
        selenium.find_element_by_id("submit_login").click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('profile_title')
        self.assertTrue(title.text.startswith('Profile'))

    # def test_profile_create_review(self):
    #     selenium = self.driver
    #     cookie = {'name': 'auth', 'value': self.auth}
    #     selenium.add_cookie(cookie)
    #     selenium.get(self.address + '/profile')
    #     print(selenium.current_url)
    #     title = selenium.find_element_by_id('profile_title')
    #     self.assertTrue(title.text.startswith('Profile'))
        try:
            reviews = selenium.find_elements_by_css_selector(".neededReview")
            count = len(reviews)
        except:
            return
        print("Count: " + str(count))
        button = selenium.find_element_by_css_selector(".createReviewButton")
        button.click()
        selenium.find_element_by_id('create_review').click()
        alert = selenium.switch_to_alert()
        print("Fill Title Error: " + alert.text)
        self.assertEqual(alert.text, "Must fill the message title")
        alert.accept()
        selenium.find_element_by_id("message-title").send_keys('Good')
        selenium.find_element_by_id('create_review').click()
        alert = selenium.switch_to_alert()
        print("Fill Body Error: " + alert.text)
        self.assertEqual(alert.text, "Must fill the message body")
        alert.accept()
        selenium.find_element_by_id('message-text').send_keys('Guy')
        selenium.find_element_by_id('create_review').click()
        print(selenium.current_url)
        reviews = selenium.find_elements_by_css_selector(".neededReview")
        # newCount = len(reviews)
        # self.assertEqual(count, newCount + 1)

    def test_signup(self):
        selenium = self.driver
        selenium.get(self.address)
        signUpNav = selenium.find_element_by_id('nav4')
        signUpNav.click()
        title = selenium.find_element_by_id('signup_title')
        self.assertEqual(title.text, "Sign Up")
        selenium.find_element_by_id('signup_submit').click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('signup_title')
        self.assertEqual(title.text, "Sign Up")
        try:
            selenium.find_element_by_id('errorMessaging')
        except:
            self.assertTrue(False, "Error messages should appear")
        selenium.find_element_by_id('username').send_keys('b')
        selenium.find_element_by_id('fname').send_keys('j')
        selenium.find_element_by_id('lname').send_keys('j')
        selenium.find_element_by_id('location').send_keys('j')
        selenium.find_element_by_id('email').send_keys('j')
        selenium.find_element_by_id('bio').send_keys('j')
        selenium.find_element_by_id('pw').send_keys('j')
        selenium.find_element_by_id('signup_submit').click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('user_title')
        self.assertTrue(title.text.startswith('User'))
        cookies = selenium.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'auth':
                logged_in = True
                break
        if not logged_in:
            self.assertTrue(False, "auth token not set")
        #Try logging out
        selenium.find_element_by_id("nav5").click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('tasktic')
        self.assertEqual(title.text, "TaskTic")
        

    def test_create_task(self):
        selenium = self.driver
        selenium.get(self.address + '/createTask')
        print(selenium.current_url)
        title = selenium.find_element_by_id('login_title')
        self.assertTrue(title.text.startswith('Login'))
        selenium.find_element_by_id("username").send_keys('user1')
        selenium.find_element_by_id("pw").send_keys('m')
        selenium.find_element_by_id("submit_login").click()
        print(selenium.current_url)
        title = selenium.find_element_by_id('createtask_title')
        self.assertTrue(title.text.startswith('Create Task'))
        selenium.find_element_by_id("createtask_submit").click()
        print(selenium.current_url) 
        #Stay on page due to error checks since no fields added
        title = selenium.find_element_by_id('createtask_title')
        self.assertEqual(title.text, "Create Task")
        try:
            selenium.find_element_by_id('errorMessaging')
        except:
            self.assertTrue(False, "Error messages should appear")
        selenium.find_element_by_id('title').send_keys('m')
        selenium.find_element_by_id('description').send_keys('m')
        selenium.find_element_by_id('location').send_keys('m')
        selenium.find_element_by_id('remote-yes').click
        selenium.find_element_by_id('time').send_keys('m')
        selenium.find_element_by_id('pricing_type_lump').click
        selenium.find_element_by_id('pricing_info').send_keys('m')
        selenium.find_element_by_id('createtask_submit').click()
        print(selenium.current_url) 
        #Stay on page because pricing_info requires int
        title = selenium.find_element_by_id('createtask_title')
        self.assertTrue(title.text.startswith('Create Task'))
        selenium.find_element_by_id('pricing_info').send_keys('1')
        selenium.find_element_by_id('createtask_submit').click()
        print(selenium.current_url)
        try: 
            title = selenium.find_element_by_id('task_title')
            self.assertTrue(title.text.startswith('Task'))
        except:
            print("No Task Redirect: " + selenium.find_element_by_id('errorMessaging').text)































    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()