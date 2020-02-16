from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Joke(models.Model):
	joke_text = models.CharField(max_length = 3000)
	pub_date = models.DateTimeField('date added')
	def __str__(self):
		return self.joke_text[22: 22 + 50]

#class User(models.Model):
#	user_name = models.CharField(max_length = 50)
#	join_date = models.DateTimeField('date joined')
#	def __str__(self):
#		return self.user_name

class Rating(models.Model):
	joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate_date = models.DateTimeField('date rated', null=True)
	rating = models.IntegerField(default = 0)

