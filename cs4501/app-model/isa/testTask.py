from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from home.models import Task

import json

class TestTask(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "db.json")
        pass #nothing to set up

    def test_asserts(self):
        self.assertEquals(1, 1)

    #Testing task_info
    def test_get_task_info(self):
        response = self.client.get(reverse('task_info', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        print(response)
        print(resp_json)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_json[0]['pk'], 1)

    def test_get_task_info_incorrect_url(self):
        response = self.client.get('/task/info/')
        self.assertEquals(response.status_code, 404)

    def test_get_task_info_not_present(self):
        response = self.client.get(reverse('task_info', args=[7]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, 'False')

    def test_post_task_info(self):
        response = self.client.post(reverse('task_info', args=[2]), '{"location":"here", "time_to_live":"2017-02-15", "post_date":"2017-02-15", "status":"OPEN", "remote":false, "pricing_type":true,"time":5}', 'raw')
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, 'True')

    #Testing task_create
    def test_task_create_get(self):
        response = self.client.get(reverse('task_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, 'False')

    def test_task_create_correct(self):
        response = self.client.post(reverse('task_create'), '{"pricing_info":"0.0", "location":"here", "time_to_live":"2017-02-15", "post_date":"2017-02-15", "status":"OPEN", "remote":false, "pricing_type":true,"time":5}', 'raw')
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json[:14], 'Created object')



    # def success_response(self):
    #     #assumes user with id 1 is stored in db
    #     response = self.client.get(reverse('all_orders_list', kwargs={'user_id':1}))

    #     #checks that response contains parameter order list & implicitly
    #     # checks that the HTTP status code is 200
    #     self.assertContains(response, 'order_list')

    # #user_id not given in url, so error
    # def fails_invalid(self):
    #     response = self.client.get(reverse('all_orders_list'))
    #     self.assertEquals(response.status_code, 404)

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down