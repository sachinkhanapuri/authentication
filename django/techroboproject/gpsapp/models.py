from django.db import models

# Create your models here.

class Vehicle(models.Model):
	checkname=models.BooleanField(default=False)
	name=models.CharField(max_length=100)
	IMEI=models.IntegerField(unique=True)
	Active=models.BooleanField(default=False)
	DateOfExpiry=models.DateField(auto_now=True)

	def __str__(self):
		return self.name
