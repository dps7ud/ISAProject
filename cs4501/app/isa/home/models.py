from django.db import models

TASK_STATUS_CHOICES = (
        ("ACC.", "Accepted"),
        ("DONE", "Done"),
        ("OPEN", "Open"),
)

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=200, default="Title")
    body = models.CharField(max_length=200, default="Body")
    score = models.FloatField(default=0) 
    task_id = models.IntegerField(default="Task")
    poster_user_id = models.IntegerField(default=0)
    postee_user_id = models.IntegerField(default=0)

class Task(models.Model):
    """Task models individual jobs (past, present or future) that
    exist within our system.
    """
    task_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    time_to_live = models.DateField()
    post_date = models.DateField()
    status = models.CharField(max_length=4, choices=TASK_STATUS_CHOICES)
    remote = models.BooleanField()
    time = models.FloatField()
    pricing_type = models.BooleanField()
    pricing_info = models.FloatField()

class Owner(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()

class TaskSkills(models.Model):
    task_id = models.IntegerField()
    # Synch max_len according to User class
    skill = models.CharField(max_length=20)

class Worker(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()

class Users(models.Model):
	fname = models.CharField(max_length=25)
	lname = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	bio = models.CharField(max_length=500)
	pw = models.CharField(max_length=50)
	location = models.CharField(max_length=50)

class UserSkills(models.Model):
	user_id = models.IntegerField()
	skill = models.CharField(max_length=25)

class UserLanguages(models.Model):
	user_id = models.IntegerField()
	spoken_language = models.CharField(max_length=50)