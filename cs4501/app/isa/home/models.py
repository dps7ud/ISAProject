from django.db import models

TASK_STATUS_CHOICES = (
        ("ACC.", "Accepted"),
        ("DONE", "Done"),
        ("OPEN", "Open"),
)

# Create your models here.
class Review(models.Model):
    task_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, default="Title")
    body = models.CharField(max_length=200, default="Body")
    score = models.FloatField(default=0) 
    poster_user_id = models.IntegerField(default=0)
    postee_user_id = models.IntegerField(default=0)

class Task(models.Model):
    """Task models individual jobs (past, present or future) that
    exist within our system.
    """
    task_id = model.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    time_to_live = models.DateField()
    post_date = models.DateField()
    status = model.CharField(max_value=4, choices=TASK_STATUS_CHOICES)
    remote = model.BooleanField()
    time = model.FloatField()
    pricing_type = model.BooleanField()
    pricing_info = model.FloatField()

class Owner(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()

class TaskSkills(models.Model):
    task_id = models.IntegerField()
    # Synch max_len according to User class
    skill = models.CharacterField(max_length=20)

class Worker(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()
