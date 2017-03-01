from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from model_app.models import Review, Task, Users, TaskSkills, Owner, Worker, UserLanguages, UserSkills

import json

class TestTask(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "./model_app/db.json")
        pass #nothing to set up

    def test_asserts(self):
        self.assertEquals(1, 1)

    #--------------------------- Testing "task_info" -------------------------------------------------
    def test_get_task_info(self):
        response = self.client.get(reverse('task_info', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_json['id'], 1)

    def test_get_task_info_incorrect_url(self):
        response = self.client.get('/task/info/')
        self.assertEquals(response.status_code, 404)

    def test_get_task_info_not_present(self):
        response = self.client.get(reverse('task_info', args=[7]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Task with that id does not exist")

    def test_post_task_info_correct_all_fields(self):
        response = self.client.post(reverse('task_info', args=[2]), {
            "location":"here", 
            "time_to_live":"2017-02-15", 
            "post_date":"2017-02-15", 
            "status":"OPEN", 
            "remote":False, 
            "pricing_type":True,
            "time":"5",
        })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "Updated task with id: 2")

    def test_post_task_info_few_fields(self):
        response = self.client.post(reverse('task_info', args=[2]), {
            "location":"here", 
            "time_to_live":"2017-02-15", 
            "post_date":"2017-02-15"
        })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "Updated task with id: 2")

    def test_post_task_info_no_id(self):
        response = self.client.post(reverse('task_info', args=[68]), {
            "location":"here", 
            "time_to_live":"2017-02-15", 
            "post_date":"2017-02-15"
        })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Task with that id does not exist")

    def test_delete_task_info_correct(self):
        response = self.client.post(reverse("task_create"), {
                "pricing_info":0.0,
                "location":"where",
                "time_to_live":"2017-02-15", 
                "title":"A hard task", 
                "description":"It is super hard", 
                "post_date":"2017-02-15", 
                "status":"OPEN", 
                "time":"5",
                "remote":False, 
                "pricing_type":True,
            })
        # response = self.client.post(reverse('task_create'), {
        #         "pricing_info":"0.0", 
        #         "location":"here", 
        #         "time_to_live":"2017-02-15", 
        #         "title":"A hard task", 
        #         "description":"It is super hard", 
        #         "post_date":"2017-02-15", 
        #         "status":"OPEN", 
        #         "time":"5",
        #         "remote":False, 
        #         "pricing_type":True
        #     })
        resp_json = json.loads((response.content).decode("utf-8"))

        response2 = self.client.delete(reverse('task_info', args=[resp_json['id']]))
        resp2 = (response2.content).decode("utf-8")
        self.assertEquals(resp2, "Deleted Task with ID: " + str(resp_json['id']))

        response3 = self.client.get(reverse('task_info', args=[resp_json['id']]))
        resp3 = (response3.content).decode("utf-8")
        self.assertEquals(resp3, "ERROR: Task with that id does not exist")

    def test_delete_task_wrong_task_id(self):
        response = self.client.delete(reverse('task_info', args=[68]))
        resp = (response.content).decode("utf-8")
        self.assertEquals(resp, "ERROR: Task with that id does not exist")

    # -------------------------------------- Testing "task_create" ----------------------------
    def test_task_create_get(self):
        response = self.client.get(reverse('task_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: task_create must be POSTed")

    def test_task_create_post_correct(self):
        response = self.client.post(reverse("task_create"), {
                "pricing_info":0.0, 
                "location":"here", 
                "time_to_live":"2017-02-15", 
                "title":"A hard task", 
                "description":"It is super hard", 
                "post_date":"2017-02-15", 
                "status":"OPEN", 
                "time": "5",
                "remote":False, 
                "pricing_type":True,
            })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_json["pricing_info"], "0.0")
        self.assertEquals(resp_json["location"], "here")
        self.assertEquals(resp_json["time_to_live"], "2017-02-15" )
        self.assertEquals(resp_json["title"], "A hard task")
        self.assertEquals(resp_json["description"], "It is super hard")
        self.assertEquals(resp_json["post_date"], "2017-02-15")
        self.assertEquals(resp_json["status"], "OPEN")
        self.assertEquals(resp_json["remote"], 'False')
        self.assertEquals(resp_json["pricing_type"], 'True')
        self.assertEquals(resp_json["time"], '5')

    def test_task_create_missing_field_required(self):
        response = self.client.post(reverse('task_create'), { 
            "location":"here", 
            "time_to_live":"2017-02-15", 
            "title":"A hard task", 
            "description":"It is super hard", 
            "post_date":"2017-02-15", 
            "status":"OPEN", 
            "remote":False, 
            "pricing_type":True,
            "time":"5.0",
        })
        resp_json = (response.content).decode("utf-8")
        self.assertTrue(resp_json.startswith("Missing required fields:"))


    # -----------------------Testing "task_skills" ------------------------------
    def test_post_task_skills(self):
        response = self.client.post(reverse('task_skills', args=[1]), {})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_task_skills_no_task(self):
        response = self.client.get(reverse('task_skills', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_task_skills_correct(self):
        response = self.client.get(reverse('task_skills', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        skillFields = tuple(field.name for field in TaskSkills._meta.fields)
        for i in resp_json:
            for j in skillFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "task_owners" ------------------------------
    def test_post_task_owners(self):
        response = self.client.post(reverse('task_owners', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_task_owners_no_task(self):
        response = self.client.get(reverse('task_owners', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_task_owners_correct(self):
        response = self.client.get(reverse('task_owners', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json:
            for j in userFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "task_workers" ------------------------------
    def test_post_task_workers(self):
        response = self.client.post(reverse('task_workers', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_task_workers_no_task(self):
        response = self.client.get(reverse('task_workers', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_task_workers_correct(self):
        response = self.client.get(reverse('task_workers', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json:
            for j in userFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "task_reviews" ------------------------------
    def test_post_task_reviews(self):
        response = self.client.post(reverse('task_reviews', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_task_reviews_no_user(self):
        response = self.client.get(reverse('task_reviews', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_task_reviews_correct(self):
        response = self.client.get(reverse('task_reviews', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json:
            for j in reviewFields:
                self.assertEquals(j in i, True)

    

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
