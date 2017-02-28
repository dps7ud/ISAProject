from django.db import models
#NEED TO PUT THESE IN THE EXPERIENCE LAYER FOR TESTING

# Create your models here.
TASK_STATUS_CHOICES = (
        ("ACC.", "Accepted"),
        ("DONE", "Done"),
        ("OPEN", "Open"),
)

# Create your models here.
class Task(models.Model):
    """Task models individual jobs (past, present or future) that
    exist within our system.
    """
    task_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #Not nullable, use ""
    location = models.CharField(max_length=200)
    time_to_live = models.DateField()
    post_date = models.DateField()
    status = models.CharField(max_length=4, choices=TASK_STATUS_CHOICES)
    remote = models.BooleanField()
    time = models.FloatField()
    pricing_type = models.BooleanField()
    pricing_info = models.FloatField()

class Users(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=500)
    pw = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

class Review(models.Model):
    title = models.CharField(max_length=200, default="Title")
    body = models.CharField(max_length=200, default="Body")
    score = models.FloatField(default=0) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    poster_user = models.ForeignKey(Users, related_name='%(class)s_poster')
    postee_user = models.ForeignKey(Users, related_name='%(class)s_postee')


class Owner(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class TaskSkills(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    skill = models.CharField(max_length=20)

class UserLanguages(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    spoken_language = models.CharField(max_length=50)

class UserSkills(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.CharField(max_length=25)

class Worker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)