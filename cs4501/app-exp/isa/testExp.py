from django.test import SimpleTestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from exp.models import Task, Review, Users, TaskSkills

import json

class TestExp(SimpleTestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        # call_command("loaddata", "db.json")
        pass #nothing to set up

    # ------------------ Testing "home" ------------------------------------
    def test_get_home(request):
        response = self.client.get(reverse('home'))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(len(resp_json[0]), 5)
        self.assertEquals(len(resp_json[1]), 5)

        #Make sure the first list is filled with Users
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json[0]:
            for j in userFields:
                self.assertEquals(j in i, True)

        #Make sure the second list is filled with Tasks
        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json[1]:
            for j in taskFields:
                self.assertEquals(j in i, True)

    def test_post_home(request):
        response = self.client.post(reverse('home'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint only accepts GET requests")

    # ------------------ Testing "review" ------------------------------------
    def test_get_review(request):
        response = self.client.get(reverse('review'), args=[1])
        resp_json = json.loads((response.content).decode("utf-8"))

        reviewFields = tuple(field.name for field in Review._meta.fields)
        for j in reviewFields:
            self.assertEquals(j in resp_json[0], True)

        #Make sure the first list is filled with Users
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json[1]:
            for j in userFields:
                self.assertEquals(j in i, True)

        for i in resp_json[2]:
            for j in userFields:
                self.assertEquals(j in i, True)

        #Make sure the second list is filled with Tasks
        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json[3]:
            for j in taskFields:
                self.assertEquals(j in i, True)

    def test_post_review(request):
        response = self.client.post(reverse('review'), args=[1])
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint only accepts GET requests")

    # ------------------ Testing "task" ------------------------------------
    def test_get_task(request):
        response = self.client.get(reverse('task'), args=[1])
        resp_json = json.loads((response.content).decode("utf-8"))

        taskFields = tuple(field.name for field in Task._meta.fields)
        for j in taskFields:
            self.assertEquals(j in resp_json[0], True)

        #Make sure the first list is filled with Users
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json[1]:
            for j in userFields:
                self.assertEquals(j in i, True)

        for i in resp_json[2]:
            for j in userFields:
                self.assertEquals(j in i, True)

        taskSkillsFields = tuple(field.name for field in TaskSkills._meta.fields)
        for i in resp_json[3]:
            for j in taskSkillsFields:
                self.assertEquals(j in i, True)

        #Make sure the second list is filled with Tasks
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json[4]:
            for j in reviewFields:
                self.assertEquals(j in i, True)

    def test_post_task(request):
        response = self.client.post(reverse('task'), args=[1])
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint only accepts GET requests")

    #----------------- Testing "user" -----------------------------------
    def test_get_user(request):
        response = self.client.get(reverse('user'), args=[1])
        resp_json = json.loads((response.content).decode("utf-8"))

        userFields = tuple(field.name for field in Users._meta.fields)
        for j in userFields:
            self.assertEquals(j in resp_json[0], True)

        #Make sure the first list is filled with Users
        userSkillsFields = tuple(field.name for field in UserSkills._meta.fields)
        for i in resp_json[2]:
            for j in userSkillsFields:
                self.assertEquals(j in i, True)

        userLanguagesFields = tuple(field.name for field in UserLanguages._meta.fields)
        for i in resp_json[1]:
            for j in userFields:
                self.assertEquals(j in i, True)

        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json[3]:
            for j in taskFields:
                self.assertEquals(j in i, True)

        for i in resp_json[4]:
            for j in taskFields:
                self.assertEquals(j in i, True)

        #Make sure the second list is filled with Tasks
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json[5]:
            for j in reviewFields:
                self.assertEquals(j in i, True)

        for i in resp_json[6]:
            for j in reviewFields:
                self.assertEquals(j in i, True)

    def test_post_user(request):
        response = self.client.post(reverse('user'), args=[1])
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint only accepts GET requests")

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down