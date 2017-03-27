from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from model_app.models import *

import json

class TestAuth(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "./model_app/db.json")

#----test authenticator create
    def test_get_auth_create(self):
        response = self.client.get(reverse('authenticator_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint must be POSTed")

        
#----test authenticator
    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
