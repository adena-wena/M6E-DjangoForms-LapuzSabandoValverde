from django.db import models # type: ignore

# Create your models here.

class Dish(models.Model):
    name = models.CharField(max_length=300)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    objects = models.Manager()
    

    def __str__(self):
        return str(self.pk) + ": " + self.name
    
class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    