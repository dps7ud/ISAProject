from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from model_app.models import Task, Review, Users

import json

class TestUtility(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "./model_app/db.json")
        pass #nothing to set up


    #----------------------Testing "get_top_five_users" ---------------------------
    def test_get_top_five_users(self):
        response = self.client.get(reverse('get_top_five_users'))
        resp_json = json.loads((response.content).decode("utf-8"))
        #Test that it returns only five users
        self.assertEquals(len(resp_json), 5)

        #Test that each object is a user
        userFields = tuple(field.name for field in Users._meta.fields)
        for i in resp_json:
            for j in userFields:
                self.assertEquals(j in i, True)

        responseRating = self.client.get(reverse('get_user_rating', args=[resp_json[0]['id']]))
        rating_json = json.loads((responseRating.content).decode("utf-8"))
        for i in range(1,5):
            responseRating2 = self.client.get(reverse('get_user_rating', 
                args=[resp_json[i]['id']]))
            rating2_json = json.loads((responseRating2.content).decode("utf-8"))
            self.assertEquals(rating2_json['rating'] <= rating_json['rating'], True)
            rating_json = rating2_json

        #Add in a new user
        create_json = {
                "username": "tester",
                "fname":'Dan',
                "lname":'Theman',
                "email":'xyz@example.com',
                "bio":"",
                "pw":'pas',
                "location":'behind you',
            }
        response = self.client.post(reverse('user_create'), 
                {
                    "username": "user99", 
                    "fname": "1", 
                    "lname": "2", 
                    "email": "3", 
                    "bio": "4", 
                    "pw": "5", 
                    "location": "6" 
                })
        print((response.content).decode("utf-8"))

        resp_json = json.loads((response.content).decode("utf-8"))

        #Add in a perfect rating for this new user
        self.client.post(reverse('review_create'), {
                "title": "",
                "body": "",
                "score": 5,
                "task": 4,
                "poster_user": 2,
                "postee_user": resp_json['id']
            })

        #Test endpoint again to make sure it works after accomodating this new user
        response = self.client.get(reverse('get_top_five_users'))
        resp_json = json.loads((response.content).decode("utf-8"))
        #Test that it returns only five users
        self.assertEquals(len(resp_json), 5)

        responseRating = self.client.get(reverse('get_user_rating', args=[resp_json[0]['id']]))
        rating_json = json.loads((responseRating.content).decode("utf-8"))
        for i in range(1,5):
            responseRating2 = self.client.get(reverse('get_user_rating', 
                args=[resp_json[i]['id']]))
            rating2_json = json.loads((responseRating2.content).decode("utf-8"))
            self.assertEquals(rating2_json['rating'] <= rating_json['rating'], True)
            rating_json = rating2_json

    def test_post_top_five_users(self):
        response = self.client.post(reverse('get_top_five_users'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    #----------------------Testing "get_recent_listings" ---------------------------
    def test_get_recent_listings(self):
        response = self.client.get(reverse('get_recent_listings'))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(len(resp_json), 5)
        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json:
            for j in taskFields:
                self.assertEquals(j in i, True)

    def test_post_recent_listings(self):
        response = self.client.post(reverse('get_recent_listings'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    #----------------------Testing "get_ruser_rating" ---------------------------
    def test_get_user_rating_known(self):
        responseRating = self.client.get(reverse('get_user_rating', args=[1]))
        rating_json = json.loads((responseRating.content).decode("utf-8"))
        self.assertEquals(rating_json['rating'], 5)

    def test_get_user_rating_no_reviews(self):
        create_json = {
                "username": "test",
                "fname":'Dan',
                "lname":'Theman',
                "email":'xyz@example.com',
                "bio":"",
                "pw":'pas',
                "location":'behind you',
            }
        response = self.client.post(reverse('user_create'), 
                {
                    "username": "user99", 
                    "fname": "1", 
                    "lname": "2", 
                    "email": "3", 
                    "bio": "4", 
                    "pw": "5", 
                    "location": "6" 
                })
        print((response.content).decode("utf-8"))

        resp_json = json.loads((response.content).decode("utf-8"))
        responseRating = self.client.get(reverse('get_user_rating', args=[resp_json['id']]))
        rating_json = json.loads((responseRating.content).decode("utf-8"))
        self.assertEquals(rating_json['rating'], 0)

    def test_get_user_rating_no_user_id(self):
        responseRating = self.client.get(reverse('get_user_rating', args=[87]))
        rating_json = json.loads((responseRating.content).decode("utf-8"))
        self.assertEquals(rating_json['rating'], 0)
    
    #----------------------Testing "authenticator_create" ---------------------------
    def test_authenticator_create_get(self):
        response = self.client.get(reverse('authenticator_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint must be POSTed")

    def test_authenticator_create_correct(self):
        response = self.client.post(reverse('authenticator_create'), {
                "username": "test",
                "authenticator": "test"
            })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json["username"], "test")
        self.assertEquals(resp_json["authenticator"], "test")

    def test_authenticator_create_missing_field(self):
        response = self.client.post(reverse('authenticator_create'), {
                "username": "test"
            })
        resp_json = (response.content).decode("utf-8")
        self.assertTrue(resp_json.startswith("Missing required fields:"))

    #----------------------Testing "authenticator_find" ---------------------------
    def test_authenticator_find_post(self):
        response = self.client.post(reverse('authenticator_find', args=["test"]), {})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json,  "ERROR: Can only accept GET requests")

    def test_authenticator_find_get_no_result(self):
        response = self.client.get(reverse('authenticator_find', args=["wrong"]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json,  "ERROR: Authenticator does not exist")

    def test_authenticator_find_get_correct(self):
        response = self.client.get(reverse('authenticator_find', args=["test"]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json[0]["username"], "user1")
        self.assertEquals(resp_json[0]["authenticator"], "test")

    #----------------------Testing "authenticator" ---------------------------
    def test_authenticator_get(self):
        response = self.client.get(reverse('authenticator', args=["test"]))
        resp_json = (response.content).decode("utf-8")
        self.assertNotEquals(resp_json, "Auth Incorrect")

    def test_authenticator_get_no_result(self):
        response = self.client.get(reverse('authenticator', args=["wrong"]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "Auth Incorrect")

    def test_authenticator_post(self):
        response = self.client.post(reverse('authenticator', args=["test"]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Not correct type of Request")

    def test_authenticator_delete_correct(self):
        response = self.client.post(reverse('authenticator_create'), {
                "username": "testing",
                "authenticator": "testing"
            })
        resp_json = json.loads((response.content).decode("utf-8"))

        response2 = self.client.delete(reverse('authenticator', args=["testing"]))
        resp2 = (response2.content).decode("utf-8")
        self.assertTrue(resp2.startswith("Deleted Authenticator:"))

        response3 = self.client.get(reverse('authenticator', args=["testing"]))
        resp_json3 = (response3.content).decode("utf-8")
        self.assertEquals(resp_json3, "Auth Incorrect")

    def test_authenticator_delete_wrong_id(self):
        response = self.client.delete(reverse('authenticator', args=["wrong"]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Authenticator with that id does not exist")




    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
