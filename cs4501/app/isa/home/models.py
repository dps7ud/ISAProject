from django.db import models

# Create your models here.
class Review(models.Model):
	title = models.CharField(max_length=200, default="Title")
	body = models.CharField(max_length=200, default="Body")
	score = models.FloatField(default=0) 
	task_id = models.IntegerField(default=0)
	poster_user_id = models.IntegerField(default=0)
	postee_user_id = models.IntegerField(default=0)

